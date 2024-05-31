Bài tập thực hành code môn Quy hoạch tuyến tính

Giáo viên hướng dẫn: Nguyễn Lê Hoàng Anh

Nhóm HNP: 

| Họ và tên  | Mã số sinh viên |
| :--- | :--- | :--- |
| Trần Minh Hiển | 21280016|
| Trần Ngọc Khánh Như | 21280040|
| Lâm Gia Phú | 21280104 |

Tổng quan:

Quy Hoạch Tuyến Tính từ lâu đã trở thành bài toán hóc búa, đòi hỏi tư duy logic và kỹ năng giải quyết vấn đề phức tạp. Nhằm đáp ứng nhu cầu ngày càng cao của việc học tập và giải quyết các bài toán quy hoạch tuyến tính hiệu quả, website HNP ra đời như một "cánh tay đắc lực" cho các bạn sinh viên trên con đường tìm tòi học hỏi của mình.  

Điểm nổi bật của website là tích hợp đầy đủ 3 thuật toán tối ưu hóa tiên tiến cho bài toán Quy Hoạch Tuyến Tính: 

Thuật toán Đơn hình: Là thuật toán giải quyết QHT theo phương pháp cổ điển, được sử dụng rộng rãi bởi tính đơn giản và hiệu quả cao. Thuật toán này hoạt động bằng cách lặp đi lặp lại các bước để tìm ra điểm cực đại hoặc cực tiểu của hàm mục tiêu, tuân theo các điều kiện ràng buộc của bài toán. 

Thuật toán Bland: Khắc phục nhược điểm của thuật toán Đơn hình, thuật toán Bland sử dụng quy tắc chọn biến đi ra khỏi cơ sở một cách linh hoạt, giúp giải quyết các bài toán quy hoạch tuyến tính phức tạp hơn, đặc biệt là khi có nhiều biến và ràng buộc. 

Thuật toán Hai pha: Phù hợp cho các bài toán quy hoạch tuyến tính có nhiều biến và ràng buộc, thuật toán Hai pha chia bài toán thành hai giai đoạn: Giai đoạn 1 biến đổi bài toán về dạng chuẩn và Giai đoạn 2 sử dụng thuật toán Đơn hình để giải quyết. 


Hướng dẫn sử dụng code:

Bước 1: Mở terminal và chỉnh đường dẫn thư mục đến file Finale

Bước 2: Kích hoạt môi trường ảo (đã có sẵn trong file code này) bằng cách chạy dòng lệnh này: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .venv\Scripts\Activate

Bước 3: Nhập : python main.py 


Lưu ý: 
Trong trường hợp chưa máy không thể chạy sau khi tải file, hãy kiểm tra xem môi trường ảo có hoạt động được không? 
Nếu không có thể không sử dụng môi trường ảo bằng cách sẽ cài đặt trực tiếp thư viện vào trong máy bằng lệnh : pip install -r requirements.txt

Sau đó nhập lệnh: python main.py 

