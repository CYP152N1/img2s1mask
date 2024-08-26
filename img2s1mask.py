import struct
import argparse
import os

# ボックスの座標を定義
BOX_COORDINATES = {
    "00": ((0, 0), (484, 194)),
    "01": ((494, 0), (980, 194)),
    "10": ((0, 212), (486, 406)),
    "11": ((494, 212), (980, 406)),
    "20": ((0, 424), (486, 618)),
    "21": ((494, 424), (980, 618)),
    "30": ((0, 636), (486, 830)),
    "31": ((494, 636), (980, 830)),
    "40": ((0, 848), (486, 1042)),
    "41": ((494, 848), (980, 1042)),
}

def read_header(file):
    header_size = 512
    file.seek(0)
    header_data = file.read(header_size).decode('utf-8', errors='ignore')
    
    # ヘッダーからサイズ情報を探す
    size1, size2 = None, None
    for line in header_data.split(';'):
        if 'SIZE1=' in line:
            size1 = int(line.split('=')[1])
        if 'SIZE2=' in line:
            size2 = int(line.split('=')[1])
    
    if size1 is None or size2 is None:
        raise ValueError("SIZE1またはSIZE2がヘッダー内に見つかりませんでした。")
    
    return size1, size2

def mask_box(outfile, x1, y1, x2, y2, size1, size2, data_type, header_size):
    data_size = struct.calcsize('<' + data_type)
    row_size = size1 * data_size
    
    # ボックス内をマスクする処理
    for y in range(y1, y2 + 1):
        row_offset = header_size + y * row_size
        
        # ファイル位置をボックス内の範囲に移動してマスクする
        outfile.seek(row_offset + x1 * data_size)
        masked_row = struct.pack('<' + data_type * (x2 - x1 + 1), *([-1] * (x2 - x1 + 1)))
        outfile.write(masked_row)

def extract_box(infile, outfile, x1, y1, x2, y2, size1, size2, data_type, header_size):
    data_size = struct.calcsize('<' + data_type)
    row_size = size1 * data_size

    # すべてを-1で初期化
    outfile.seek(header_size)
    outfile.write(struct.pack('<' + data_type * (size1 * size2), *([-1] * (size1 * size2))))

    # ボックス内のピクセルをコピーする
    for y in range(y1, y2 + 1):
        row_offset = header_size + y * row_size
        infile.seek(row_offset + x1 * data_size)
        pixel_data = infile.read((x2 - x1 + 1) * data_size)

        outfile.seek(row_offset + x1 * data_size)
        outfile.write(pixel_data)

def modify_binary_data(args):
    header_size = 512
    data_type = 'l'  # long integer (4 bytes)

    # 入力ファイル名のベース名を取得し、出力ファイル名を生成
    input_basename = os.path.splitext(args.file)[0]

    if args.box:
        # ボックス処理
        output_file_path = f"{input_basename}_modified_box.img"
        with open(args.file, 'rb') as infile, open(output_file_path, 'wb') as outfile:
            # ファイル全体をコピー
            outfile.write(infile.read())

        with open(output_file_path, 'r+b') as outfile:
            # ヘッダーからサイズを読み込む
            size1, size2 = read_header(outfile)
            print(f"Read from header: SIZE1={size1}, SIZE2={size2}")

            new_value = -1 if args.mask else args.i

            # ボックス範囲をマスクする
            mask_box(outfile, args.x1, args.y1, args.x2, args.y2, size1, size2, data_type, header_size)

    elif args.box_mask or args.box_extract:
        if args.box_mask:
            box_label = args.box_mask
            output_file_path = f"{input_basename}_box{box_label}mask.img"
        elif args.box_extract:
            box_label = args.box_extract
            output_file_path = f"{input_basename}_box{box_label}extract.img"

        if box_label not in BOX_COORDINATES:
            raise ValueError(f"無効なボックスID: {box_label}")

        # 出力ファイルを開く
        with open(args.file, 'rb') as infile, open(output_file_path, 'wb') as outfile:
            # ファイル全体をコピー
            outfile.write(infile.read())

        # ヘッダーからサイズを読み込む
        with open(output_file_path, 'r+b') as outfile:
            size1, size2 = read_header(outfile)
            print(f"Read from header: SIZE1={size1}, SIZE2={size2}")

            # ボックスの座標を取得
            x1, y1 = BOX_COORDINATES[box_label][0]
            x2, y2 = BOX_COORDINATES[box_label][1]

            # ボックスマスクまたは抽出を実行
            if args.box_mask:
                mask_box(outfile, x1, y1, x2, y2, size1, size2, data_type, header_size)
            elif args.box_extract:
                with open(args.file, 'rb') as infile:
                    extract_box(infile, outfile, x1, y1, x2, y2, size1, size2, data_type, header_size)

if __name__ == '__main__':
    # コマンドライン引数のパーサーを設定
    parser = argparse.ArgumentParser(description="バイナリデータを座標指定で書き換えるプログラム")

    # ファイルの指定
    parser.add_argument('file', type=str, help="入力するバイナリファイルのパス")

    # 単一ピクセル/ボックス範囲の書き換え用引数
    parser.add_argument('-x', type=int, help="X座標")
    parser.add_argument('-y', type=int, help="Y座標")
    
    # ボックス単位での書き換え用引数
    parser.add_argument('--box', '-b', action='store_true', help="範囲を指定して書き換えるモードを有効にする")
    parser.add_argument('-x1', type=int, help="ボックスの左上のX座標", required=False)
    parser.add_argument('-y1', type=int, help="ボックスの左上のY座標", required=False)
    parser.add_argument('-x2', type=int, help="ボックスの右下のX座標", required=False)
    parser.add_argument('-y2', type=int, help="ボックスの右下のY座標", required=False)

    # ボックスマスクとボックス以外のマスクの引数
    parser.add_argument('-bm', '--box-mask', type=str, help="特定のボックスをマスクする (例: 00, 41)", required=False)
    parser.add_argument('-be', '--box-extract', type=str, help="特定のボックス以外をマスクする (例: 00, 41)", required=False)

    # 共通の引数: -i または -m/--mask
    group = parser.add_mutually_exclusive_group(required=not (parser.parse_known_args()[0].box_mask or parser.parse_known_args()[0].box_extract))
    group.add_argument('-i', type=int, help="書き込む新しい値")
    group.add_argument('-m', '--mask', action='store_true', help="-1を自動的に設定")

    args = parser.parse_args()

    # バリデーション
    if args.box_mask and args.box_extract:
        parser.error("ボックスマスクとボックス抽出を同時に指定することはできません")

    if args.box:
        if args.x1 is None or args.y1 is None or args.x2 is None or args.y2 is None:
            parser.error("--boxモードでは-x1, -y1, -x2, -y2を指定する必要があります")
    elif not args.box_mask and not args.box_extract:
        if args.x is None or args.y is None:
            parser.error("単一ピクセルモードでは-xと-yを指定する必要があります")

    # バイナリデータを変換
    modify_binary_data(args)

