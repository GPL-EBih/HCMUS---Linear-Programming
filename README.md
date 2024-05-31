
# Bài Tập Thực Hành Code Môn Quy Hoạch Tuyến Tính

**Giáo viên hướng dẫn:** Nguyễn Lê Hoàng Anh

## Nhóm HNP:

| Họ và tên           | Mã số sinh viên |
|---------------------|-----------------|
| Trần Minh Hiển      | 21280016        |
| Trần Ngọc Khánh Như | 21280040        |
| Lâm Gia Phú         | 21280104        |

## Tổng Quan:

Quy Hoạch Tuyến Tính từ lâu đã trở thành bài toán hóc búa, đòi hỏi tư duy logic và kỹ năng giải quyết vấn đề phức tạp. Nhằm đáp ứng nhu cầu ngày càng cao của việc học tập và giải quyết các bài toán quy hoạch tuyến tính hiệu quả, website HNP ra đời như một "cánh tay đắc lực" cho các bạn sinh viên trên con đường tìm tòi học hỏi của mình.  

Điểm nổi bật của website là tích hợp đầy đủ 3 thuật toán tối ưu hóa tiên tiến cho bài toán Quy Hoạch Tuyến Tính: 

1. **Thuật toán Đơn hình:** Là thuật toán giải quyết QHT theo phương pháp cổ điển, được sử dụng rộng rãi bởi tính đơn giản và hiệu quả cao. Thuật toán này hoạt động bằng cách lặp đi lặp lại các bước để tìm ra điểm cực đại hoặc cực tiểu của hàm mục tiêu, tuân theo các điều kiện ràng buộc của bài toán. 

2. **Thuật toán Bland:** Khắc phục nhược điểm của thuật toán Đơn hình, thuật toán Bland sử dụng quy tắc chọn biến đi ra khỏi cơ sở một cách linh hoạt, giúp giải quyết các bài toán quy hoạch tuyến tính phức tạp hơn, đặc biệt là khi có nhiều biến và ràng buộc. 

3. **Thuật toán Hai pha:** Phù hợp cho các bài toán quy hoạch tuyến tính có nhiều biến và ràng buộc, thuật toán Hai pha chia bài toán thành hai giai đoạn: Giai đoạn 1 biến đổi bài toán về dạng chuẩn và Giai đoạn 2 sử dụng thuật toán Đơn hình để giải quyết. 

## Sử dụng trực tiếp sản phẩm qua website:
Truy cập đường dẫn : https://hcmus-linear-programming.onrender.com/

Quá trình truy cập có thể mất khoảng 5 phút cho lần truy cập đầu, nếu sau khoảng 50 phút không sử dụng trang web sẽ cần được reload lại do gói VPS còn hạn chế.

## Hướng Dẫn Sử Dụng Code:

1. **Mở terminal và chỉnh đường dẫn thư mục đến file `Finale`.**

2. **Kích hoạt môi trường ảo:**
    - Nếu bạn đang sử dụng Windows, chạy lệnh sau để kích hoạt môi trường ảo:
      ```bash
      Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .venv\Scripts\Activate
      ```
    - Nếu bạn đang sử dụng macOS hoặc Linux, chạy lệnh sau:
      ```bash
      source .venv/bin/activate
      ```

3. **Chạy chương trình:**
    ```bash
    python main.py
    ```

## Lưu Ý:
- Trong trường hợp không thể chạy được sau khi tải file, hãy kiểm tra xem môi trường ảo có hoạt động không.
- Nếu môi trường ảo không hoạt động, bạn có thể cài đặt trực tiếp các thư viện vào máy bằng lệnh:
  ```bash
  pip install -r requirements.txt
  ```
  Sau đó, chạy lại chương trình:
  ```bash
  python main.py
  ```


