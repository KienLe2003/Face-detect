# Face Anonymization Application

Ứng dụng Python này cho phép bạn ẩn danh các khuôn mặt được phát hiện từ luồng webcam bằng các phương pháp khác nhau (Làm mờ, Pixel hóa hoặc Thay thế bằng Emoji). Ứng dụng cung cấp một giao diện đồ họa người dùng (GUI) với các nút để chuyển đổi giữa các phương pháp ẩn danh và một thanh điều chỉnh để điều chỉnh độ mờ.

## Features

-  **Face Detection**: Sử dụng Haar Cascades để phát hiện khuôn mặt trong thời gian thực thông qua webcam.
- **Anonymization Methods**
  - **Blur**: Làm mờ các khuôn mặt được phát hiện, với khả năng điều chỉnh cường độ làm mờ.
  - **Pixelate**: Pixel hóa các khuôn mặt được phát hiện để ẩn danh.
  - **Emoji Replacement**: Thay thế các khuôn mặt được phát hiện bằng một hình ảnh emoji.
- **Real-Time Preview**: Hiển thị luồng webcam sống với phương pháp ẩn danh đã được áp dụng.
- **Adjustable Blur Level**: Có một thanh điều chỉnh để kiểm soát mức độ làm mờ được áp dụng cho các khuôn mặt.

## Requirements

- Python 3.12.6 64bit
- OpenCV
- NumPy
- Pillow
- Tkinter (đi kèm với Python)


   ```bash
   pip install opencv-python numpy pillow
