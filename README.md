# ADXVで出力された32bit_imgのマスクプログラム README

## 概要

このプログラムは、512バイトのヘッダーを持つ、long_integerのlittle_endian形式のバイナリファイルに対して、特定の矩形領域（ボックス）をマスクまたは抽出する機能を提供します。指定されたボックス内のピクセルをマスクしたり、ボックス以外の領域をすべてマスクすることが可能です。また、ボックス内の個々のピクセル値を変更することもできます。

## 機能

- **特定のボックスのマスキング:** 事前に定義されたボックス内のピクセルをマスク（-1）します。
- **ボックスの抽出:** 指定されたボックス内のピクセルを保持し、その他の領域をマスク（-1）します。
- **ピクセルの書き換え:** ボックス内の特定の座標にあるピクセルの値を新しい値に書き換えます。
- **ヘッダーの解析:** バイナリファイルのヘッダーから画像のサイズ情報（`SIZE1`, `SIZE2`）を自動的に取得します。

## ボックス座標

以下は事前に定義されたボックス座標の一覧です：

- **00:** (0, 0) から (484, 194) まで
- **01:** (494, 0) から (980, 194) まで
- **10:** (0, 212) から (486, 406) まで
- **11:** (494, 212) から (980, 406) まで
- **20:** (0, 424) から (486, 618) まで
- **21:** (494, 424) から (980, 618) まで
- **30:** (0, 636) から (486, 830) まで
- **31:** (494, 636) から (980, 830) まで
- **40:** (0, 848) から (486, 1042) まで
- **41:** (494, 848) から (980, 1042) まで

## 必要条件

- Python 3.x
- 標準ライブラリ（`struct`、`argparse`、`os`）のみ使用

## 使い方

### 基本コマンド

```bash
python img2s1mask.py <binary_file_path> -x <x座標> -y <y座標> -i <新しい値>
```

指定された座標 `(x, y)` のピクセルを新しい値 `<新しい値>` に書き換えます。

### ボックスのマスキング

```bash
python img2s1mask.py <binary_file_path> -bm <ボックスラベル>
```

指定されたボックス（例: `00`, `41`）内のピクセルを `-1` でマスクします。

### ボックスの抽出

```bash
python img2s1mask.py <binary_file_path> -be <ボックスラベル>
```

指定されたボックス内のピクセルを保持し、それ以外の領域を `-1` でマスクします。

### カスタム座標でのボックス変更

```bash
python img2s1mask.py <binary_file_path> --box -x1 <x1> -y1 <y1> -x2 <x2> -y2 <y2> -i <新しい値>
```

矩形領域 `(x1, y1)` から `(x2, y2)` の全ピクセルを新しい値 `<新しい値>` に書き換えます。

### 特定のエリアのマスキング

```bash
python img2s1mask.py <binary_file_path> --box -x1 <x1> -y1 <y1> -x2 <x2> -y2 <y2> -m
```

矩形領域 `(x1, y1)` から `(x2, y2)` の全ピクセルをマスクします。

### ボックス抽出

```bash
python img2s1mask.py <binary_file_path> -be <ボックスラベル>
```

指定されたボックス内のピクセルを保持し、それ以外をマスクします。

## 例

- ボックス `00` をマスクする場合：
    ```bash
    python img2s1mask.py input_file.img -bm 00
    ```

- ボックス `11` を抽出し、それ以外のピクセルをマスクする場合：
    ```bash
    python img2s1mask.py input_file.img -be 11
    ```

- カスタムエリアのピクセルを変更する場合：
    ```bash
    python img2s1mask.py input_file.img --box -x1 50 -y1 50 -x2 100 -y2 100 -i 1234
    ```

## エラーハンドリング

- プログラムはすべての入力を検証し、無効な引数（不正なボックスラベルや座標の不足）についてエラーメッセージを出力します。

## 作者

Hiroki Onoda Nagoya University
ChatGPT4o

## ライセンス

このプロジェクトは MIT License の下でライセンスされています。

---

# README for Binary Data Box Masking Program

## Overview

This program processes binary image files by masking or extracting specific rectangular areas (boxes) based on their coordinates. The program is capable of applying masks to a specific box, extracting everything except a specific box, or modifying individual pixel values within the box.

## Features

- **Masking a Specific Box:** Apply a mask (-1) to pixels within a predefined box.
- **Extracting a Box:** Keep the pixels inside a predefined box and mask all other pixels (-1).
- **Modifying Pixels:** Set individual pixel values inside the specified box or specific coordinates.
- **Header Parsing:** Automatically reads the header from the binary file to obtain the image dimensions (`SIZE1`, `SIZE2`).

## Box Coordinates

The predefined box coordinates are as follows:

- **00:** From (0, 0) to (484, 194)
- **01:** From (494, 0) to (980, 194)
- **10:** From (0, 212) to (486, 406)
- **11:** From (494, 212) to (980, 406)
- **20:** From (0, 424) to (486, 618)
- **21:** From (494, 424) to (980, 618)
- **30:** From (0, 636) to (486, 830)
- **31:** From (494, 636) to (980, 830)
- **40:** From (0, 848) to (486, 1042)
- **41:** From (494, 848) to (980, 1042)

## Requirements

- Python 3.x
- No external libraries required (only built-in libraries like `struct`, `argparse`, and `os`).

## Usage

### Basic Command

```bash
python img2s1mask.py <binary_file_path> -x <x_coordinate> -y <y_coordinate> -i <new_value>
```

This command modifies a single pixel at the given coordinates `(x, y)` with the new value `<new_value>`.

### Masking a Box

```bash
python img2s1mask.py <binary_file_path> -bm <box_label>
```

This command masks the pixels within the specified box (e.g., `00`, `41`) with `-1`.

### Extracting a Box

```bash
python img2s1mask.py <binary_file_path> -be <box_label>
```

This command retains the pixels within the specified box and masks all other areas with `-1`.

### Box Modification with Custom Coordinates

```bash
python img2s1mask.py <binary_file_path> --box -x1 <x1> -y1 <y1> -x2 <x2> -y2 <y2> -i <new_value>
```

This command modifies all pixels within the rectangular area defined by the coordinates `(x1, y1)` and `(x2, y2)` with the new value `<new_value>`.

### Masking a Specific Area

```bash
python img2s1mask.py <binary_file_path> --box -x1 <x1> -y1 <y1> -x2 <x2> -y2 <y2> -m
```

This command masks all pixels in the area defined by `(x1, y1)` and `(x2, y2)`.

### Box Extraction

```bash
python img2s1mask.py <binary_file_path> -be <box_label>
```

This command retains the pixels inside the specified box while masking everything else.

## Example Commands

- To mask the box labeled `00`:
    ```bash
    python img2s1mask.py input_file.img -bm 00
    ```

- To extract the box labeled `11` and mask the rest of the image:
    ```bash
    python img2s1mask.py input_file.img -be 11
    ```

- To modify pixels within a custom area:
    ```bash
    python img2s1mask.py input_file.img --box -x1 50 -y1 50 -x2 100 -y2 100 -i 1234
    ```

## Error Handling

- The program validates all inputs and throws errors for invalid arguments such as incorrect box labels or missing required coordinates.
  
## Author

Developed by [Hiroki Onoda] & [ChatGPT4o]

## License

This project is licensed under the MIT License.

---

Feel free to customize the README as per your specific needs!
