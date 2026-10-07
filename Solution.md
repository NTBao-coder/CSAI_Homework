# Solution — HomeWork 1: Search

**Student ID:** 24120023  
**Name:** Nguyễn Thành Bảo  
**Email:** 24120023@student.hcmus.edu.vn  
**Nguồn đề:** `HomeWork_1_Search.pdf`, trang 1–2.  
**Phạm vi:** lời giải chi tiết cho cả hai câu; bản báo cáo được trình bày lại từ file này trong `latex/main.tex`.

## 1. Đọc và mô hình hóa đúng đề

Bản đồ có bốn cột A, B, C, D từ trái sang phải và năm hàng 1–5 từ dưới lên trên. Các ô trắng đi được, các ô đen không đi được.

```text
          A       B       C       D
    5     A5      B5      C5      D5
    4     A4       #       #      D4
    3     A3      B3      C3      D3
    2      #      B2       #       #
    1      #      B1       #       #
```

- Xuất phát: B1.
- Bạn 1: A3. Bạn 2: D3. Boss: C5.
- Chỉ được đi **Up, Left, Right**, mỗi lần sang một ô trắng kề cạnh; **không được đi Down**.
- Mỗi bước tốn một đơn vị năng lượng.
- Phải đón **cả hai** người bạn trước khi hoàn thành mục tiêu tại C5. Không có chi phí riêng cho hành động đón bạn hay đánh boss trong đề.

Đây là đồ thị có hướng: từ A3 đi lên A4 được, nhưng từ A4 không thể quay xuống A3. Các cạnh ngang giữa hai ô trắng cho phép đi cả hai chiều.

Nếu tìm kiếm toàn bộ bài toán trong một lần, trạng thái phải là `(vị trí, tập bạn đã đón)`. Ví dụ `(B3, ∅)` và `(B3, {A3})` là hai trạng thái khác nhau. Đích thực sự là `(C5, {A3, D3})`. Chỉ dùng tên ô làm trạng thái của toàn bài sẽ có thể loại nhầm một lần quay lại cần thiết.

## 2. Answers — Câu 1: bảng khoảng cách Manhattan

### 2.1. Công thức

Gán A = 1, B = 2, C = 3, D = 4; chỉ số hàng chính là tọa độ y. Với hai ô P = (xP, yP), Q = (xQ, yQ):

\[
d_M(P,Q)=|x_P-x_Q|+|y_P-y_Q|.
\]

Đây là tổng độ lệch ngang và dọc, chưa tính chướng ngại vật và chiều di chuyển. Không thay các giá trị bằng độ dài đường đi vòng.

### 2.2. Kết quả theo đúng thứ tự cột của đề

| Đích / Ô | A3 | A4 | A5 | B1 | B2 | B3 | B5 | C3 | C5 | D3 | D4 | D5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Friend 1 (A3) | 0 | 1 | 2 | 3 | 2 | 1 | 3 | 2 | 4 | 3 | 4 | 5 |
| Friend 2 (D3) | 3 | 4 | 5 | 4 | 3 | 2 | 4 | 1 | 3 | 0 | 1 | 2 |
| Big boss (C5) | 4 | 3 | 2 | 5 | 4 | 3 | 1 | 2 | 0 | 3 | 2 | 1 |

Ví dụ tính tay:

- B1 → A3: `|2−1| + |1−3| = 1+2 = 3`.
- B1 → D3: `|2−4| + |1−3| = 2+2 = 4`.
- B1 → C5: `|2−3| + |1−5| = 1+4 = 5`.
- A4 → D3: `|1−4| + |4−3| = 3+1 = 4`.
- D5 → A3: `|4−1| + |5−3| = 3+2 = 5`.

Hai ô B4, C4 bị chặn không xuất hiện trong bảng. Manhattan vẫn hữu hạn cho những cặp không thể đi tới: A4 → D3 có khoảng cách Manhattan 4, nhưng không có đường đi hợp lệ vì phải giảm hàng từ 4 xuống 3. Đây không phải lỗi của bảng; heuristic là cận dưới, không phải phép kiểm tra khả năng tới đích.

## 3. Answers — Câu 2: chọn chiến lược và chứng minh thứ tự

### 3.1. Vì sao không chỉ chạy A* từ B1 tới C5?

Đường tới C5 có thể bỏ qua bạn ở A3 hoặc D3. Ví dụ B1 → B2 → B3 → C3 → D3 → D4 → D5 → C5 chỉ mất 7 bước nhưng thiếu bạn ở A3, nên không phải lời giải của đề.

Đề cho phép dùng nhiều cây tìm kiếm. Ta dùng ba lượt A* với các đích cố định, sau khi so sánh cả hai thứ tự đón bạn. Không suy ra tối ưu toàn cục chỉ từ việc chọn người bạn gần nhất.

### 3.2. So sánh cả hai thứ tự có thể

**Thứ tự I: B1 → A3 → D3 → C5.** Mọi đường có thứ tự đón này đều có chi phí ít nhất

\[
d_M(B1,A3)+d_M(A3,D3)+d_M(D3,C5)=3+3+3=9.
\]

Cận dưới đạt được bởi ba đoạn hợp lệ:

1. B1 → B2 → B3 → A3: 3 bước.
2. A3 → B3 → C3 → D3: 3 bước.
3. D3 → D4 → D5 → C5: 3 bước.

**Thứ tự II: B1 → D3 → A3 → C5.** Mọi đường có thứ tự đón này đều có chi phí ít nhất

\[
d_M(B1,D3)+d_M(D3,A3)+d_M(A3,C5)=4+3+4=11.
\]

Cận dưới cũng đạt được:

1. B1 → B2 → B3 → C3 → D3: 4 bước.
2. D3 → C3 → B3 → A3: 3 bước.
3. A3 → A4 → A5 → B5 → C5: 4 bước.

Mọi lời giải có một trong hai thứ tự **đón lần đầu** trên. Vì vậy chi phí tối ưu toàn cục là `min(9, 11) = 9`. Quay lại thêm ô hoặc đón lại một người bạn không thể hạ các cận dưới này. Kết luận có xét đầy đủ việc không được đi xuống: cả hai đường đạt cận dưới vừa nêu đều chỉ dùng Up, Left, Right.

Sau khi đón A3 trước, phải đi ngang sang D3 ở hàng 3; nếu đi lên A4, mèo không thể quay về hàng 3 để đón D3.

### 3.3. Heuristic cho ba cây

| Lượt | Xuất phát | Đích | Heuristic | Chi phí đã dùng trước lượt |
|---|---|---|---|---:|
| 1 | B1 | A3 | h₁(n) = dM(n, A3) | 0 |
| 2 | A3 | D3 | h₂(n) = dM(n, D3) | 3 |
| 3 | D3 | C5 | h₃(n) = dM(n, C5) | 6 |

Trong mỗi cây, `g` tính **từ gốc của cây đó**, gốc có g = 0, và `f = g+h`. Không nhầm g cục bộ này với tổng năng lượng tính từ B1. Nếu dùng chi phí tích lũy toàn hành trình, cộng lần lượt 0, 3, 6 vào cả f và g của các cây tương ứng; h giữ nguyên.

### 3.4. Tính chấp nhận được và nhất quán

Với đích cố định t, mỗi bước kề cạnh chỉ thay đổi một tọa độ đúng một đơn vị. Do đó mọi đường hợp lệ từ n tới t dài ít nhất dM(n,t), tức `h(n) ≤ h*(n)`. Chướng ngại vật và việc cấm đi xuống chỉ có thể làm đường ngắn nhất dài hơn hoặc khiến đích không thể tới được, chứ không làm cận dưới tăng quá chi phí thật.

Với mọi cạnh hợp lệ n → n′ có chi phí 1, bất đẳng thức tam giác cho:

\[
h(n)=d_M(n,t)\le d_M(n,n')+d_M(n',t)=1+h(n').
\]

Ngoài ra h(t)=0. Heuristic Manhattan vì vậy nhất quán và chấp nhận được cho từng lượt. A* graph-search kết thúc khi lấy đích khỏi OPEN sẽ cho đường ngắn nhất của lượt đó. Chứng minh tối ưu **toàn bài** vẫn cần phép so sánh hai thứ tự ở mục 3.2.

### 3.5. Quy ước tái hiện cây và xử lý nút trùng

1. OPEN ưu tiên f nhỏ nhất; nếu bằng f, chọn h nhỏ nhất; nếu vẫn bằng, chọn nút được đưa vào OPEN trước.
2. Sinh các nút con theo thứ tự **Up → Left → Right**. Bỏ ô đen và ô ngoài bản đồ.
3. Lưu g tốt nhất cho từng ô trong một lượt. Nếu nút đã có g không lớn hơn g mới, loại bản sao mới; không đưa vào OPEN.
4. OPEN và CLOSED được khởi tạo lại ở mỗi lượt. Nhờ đó B3 đã qua ở lượt 1 vẫn có thể được dùng ở lượt 2.
5. Kiểm tra đích khi **lấy nút ra khỏi OPEN**, không dừng ngay khi mới sinh đích.
6. Dừng cây ngay khi lấy đích ra; không tiếp tục sinh con của đích hoặc mở rộng các nhánh còn chờ.

Trong các cây dưới đây, mỗi nút đều có **(f,g,h)**. Dấu `★` đánh dấu đường được chọn; `OPEN` là nút còn chờ tại lúc dừng; `loại` là bản sao có g lớn hơn giá trị đã biết. Bảng OPEN được sắp theo quy tắc ưu tiên trên.

## 4. Cây A* 1 — B1 tới A3

Heuristic h₁(n) = dM(n,A3).

```text
★ B1 (3,0,3)
  └─ Up → ★ B2 (3,1,2)
             └─ Up → ★ B3 (3,2,1)
                        ├─ Left  → ★ A3 (3,3,0) [đích]
                        └─ Right →   C3 (5,3,2) [OPEN]
```

| Lần lấy | Nút lấy khỏi OPEN | OPEN sau xử lý |
|---:|---|---|
| 1 | B1 (3,0,3) | B2 (3,1,2) |
| 2 | B2 (3,1,2) | B3 (3,2,1) |
| 3 | B3 (3,2,1) | A3 (3,3,0); C3 (5,3,2) |
| 4 | A3 (3,3,0) | Dừng; C3 (5,3,2) còn chờ |

Tại B3, Up là B4 bị chặn. Hai nút hợp lệ là A3 và C3. Với C3, g = 3 và h₁ = |3−1| + |3−3| = 2 nên f = 5; vì thế A3 với f = 3 được chọn trước.

**Đường đoạn 1:** B1 → B2 → B3 → A3. Chi phí 3. Đã đón bạn 1.

## 5. Cây A* 2 — A3 tới D3

Khởi tạo lượt mới tại A3, g = 0; h₂(n) = dM(n,D3).

```text
★ A3 (3,0,3)
  ├─ Up    →   A4 (5,1,4) [OPEN]
  └─ Right → ★ B3 (3,1,2)
                ├─ Left  → A3 (5,2,3) [loại: 2 > 0]
                └─ Right → ★ C3 (3,2,1)
                              ├─ Left  → B3 (5,3,2) [loại: 3 > 1]
                              └─ Right → ★ D3 (3,3,0) [đích]
```

| Lần lấy | Nút lấy khỏi OPEN | OPEN sau xử lý |
|---:|---|---|
| 1 | A3 (3,0,3) | B3 (3,1,2); A4 (5,1,4) |
| 2 | B3 (3,1,2) | C3 (3,2,1); A4 (5,1,4) |
| 3 | C3 (3,2,1) | D3 (3,3,0); A4 (5,1,4) |
| 4 | D3 (3,3,0) | Dừng; A4 (5,1,4) còn chờ |

- A4 có g = 1, h₂ = |1−4| + |4−3| = 4, nên f = 5. Nhánh này không được mở rộng trước khi tìm ra D3.
- B3 → A3 tạo g mới bằng 2, lớn hơn g(A3) = 0; bản sao A3 bị loại.
- C3 → B3 tạo g mới bằng 3, lớn hơn g(B3) = 1; bản sao B3 bị loại.
- B4 và C4 bị chặn, nên không có nhánh Up từ B3 hoặc C3.

Hai nút bị loại được vẽ để thể hiện đầy đủ các phép sinh nút; chúng không thuộc OPEN. A4 vẫn có heuristic hữu hạn mặc dù từ hàng 4 không thể về D3 ở hàng 3.

**Đường đoạn 2:** A3 → B3 → C3 → D3. Chi phí riêng 3, tích lũy 6. Đã có cả hai bạn.

## 6. Cây A* 3 — D3 tới C5

Khởi tạo lượt mới tại D3, g = 0; h₃(n) = dM(n,C5).

```text
★ D3 (3,0,3)
  ├─ Up   → ★ D4 (3,1,2)
  │            └─ Up → ★ D5 (3,2,1)
  │                       └─ Left → ★ C5 (3,3,0) [đích]
  └─ Left →   C3 (3,1,2) [OPEN]
```

| Lần lấy | Nút lấy khỏi OPEN | OPEN sau xử lý |
|---:|---|---|
| 1 | D3 (3,0,3) | D4 (3,1,2); C3 (3,1,2) |
| 2 | D4 (3,1,2) | D5 (3,2,1); C3 (3,1,2) |
| 3 | D5 (3,2,1) | C5 (3,3,0); C3 (3,1,2) |
| 4 | C5 (3,3,0) | Dừng; C3 (3,1,2) còn chờ |

D4 và C3 ban đầu cùng (3,1,2). D4 được đưa vào trước do ưu tiên sinh Up trước Left, nên được chọn trước. Sau đó D5 và C3 cùng f = 3, nhưng h(D5) = 1 < 2 nên chọn D5. Tương tự, C5 có h = 0 nên được lấy trước C3.

Việc C3 còn trong OPEN không ảnh hưởng tính tối ưu: thuật toán đã lấy đích C5 có f = g = 3 nhỏ nhất. Nếu chọn quy tắc hòa khác, thứ tự mở rộng và hình dạng cây có thể khác, nhưng chi phí tối ưu của đoạn vẫn là 3.

**Đường đoạn 3:** D3 → D4 → D5 → C5. Chi phí riêng 3, tích lũy 9. Đã có đủ hai bạn trước khi gặp boss.

## 7. Đáp án cuối cùng và kiểm tra

### 7.1. Đường đi tốt nhất

\[
B1\to B2\to B3\to A3\to B3\to C3\to D3\to D4\to D5\to C5.
\]

Dãy hành động: **Up, Up, Left, Right, Right, Right, Up, Up, Left**.

Có 10 lần xuất hiện ô trên hành trình, nhưng chỉ có **9 cạnh**, nên dùng **9 đơn vị năng lượng**. B3 xuất hiện hai lần là hợp lệ và cần thiết: sau khi đón A3 phải quay ngang qua B3 để tới D3. Không hề có bước đi xuống.

| Bước / năng lượng tích lũy | Vị trí | Bạn đã đón |
|---:|---|---|
| 0 | B1 | Chưa có |
| 1 | B2 | Chưa có |
| 2 | B3 | Chưa có |
| 3 | A3 | A3 |
| 4 | B3 | A3 |
| 5 | C3 | A3 |
| 6 | D3 | A3, D3 |
| 7 | D4 | A3, D3 |
| 8 | D5 | A3, D3 |
| 9 | C5 | A3, D3; hoàn thành |

### 7.2. Đối chiếu bằng thuật toán độc lập

File `tools/verify_search.py` chỉ dùng thư viện chuẩn Python. Chạy:

```bash
python3 tools/verify_search.py
```

Script tính lại toàn bộ 36 giá trị Manhattan; chạy A* với đúng quy tắc hòa để in các nút được lấy ra và các nút được sinh, kể cả bản sao bị loại; kiểm tra các cạnh của đường kết quả; kiểm tra tính nhất quán của heuristic trên mọi cạnh; và kiểm tra thứ tự ngược có chi phí 11.

Quan trọng hơn, script chạy **BFS độc lập** trên đồ thị trạng thái `(vị trí, mặt nạ bạn)` với mặt nạ 0 = chưa có bạn, 1 = có A3, 2 = có D3, 3 = có cả hai. Trạng thái đầu là `(B1,0)`, trạng thái đích là `(C5,3)`. BFS không dùng Manhattan, không cố định thứ tự đón bạn và không chia bài toán thành ba đoạn. Vì mọi cạnh có chi phí 1, khoảng cách BFS là chi phí tối ưu của toàn bài. Kết quả xác nhận đúng đường trên với chi phí **9**.

### 7.3. Những lỗi cần tránh khi trình bày

- Đi xuống hoặc đi vào B4/C4 hay các ô đen khác.
- Dừng tại C5 khi chưa đón đủ hai bạn.
- Dùng riêng dM(n,C5) rồi bỏ qua trạng thái đón bạn.
- Cộng khoảng cách tới cả ba đích mà không chứng minh đó là heuristic chấp nhận được cho trạng thái đầy đủ.
- Đánh dấu B3 là đã thăm vĩnh viễn cho toàn hành trình và cấm quay lại sau khi đón A3.
- Cộng g của các nút trên đường thay vì đếm cạnh; tổng chi phí là 3+3+3, không phải tổng mọi g.
- Khẳng định chọn bạn gần nhất luôn tối ưu; trong bài này kết luận dựa trên so sánh đủ hai thứ tự.
- Ghi tuple theo thứ tự (g,h,f) thay vì **(f,g,h)** mà đề yêu cầu.

## 8. Quy cách bản báo cáo nộp

Báo cáo dùng mẫu FIT–HCMUS trong dự án, A4, lề trái 30 mm / phải 20 mm / trên và dưới 20 mm, chữ Times New Roman 13 pt, giãn dòng 1,35. Dùng bố cục bài tập cá nhân, có Student ID, Name, Answers với đúng hai câu trả lời. Ba cây A* thể hiện đầy đủ tuple, nhánh được chọn, nút còn chờ và bản sao bị loại. File PDF cuối cùng mang tên **`24120023.pdf`** đúng yêu cầu trang 2 của đề.

Thông tin lớp hiện dùng **CQ024/22** theo `My_Information.md`; giảng viên **ThS. Bùi Tiến Lên** và mã môn **CSC10043** được giữ theo cấu hình `main.tex` do người dùng cung cấp. Bản báo cáo đã biên dịch gồm **8 trang**. Trang 1 dùng bố cục trang bìa của **templateFirtPage.pdf**, gồm tên trường/khoa, logo, môn học, tên bài trong khung và thông tin giảng viên/sinh viên; giữ họ tên, MSSV, email và lớp của người làm bài. Phần giải **Câu 1: Khoảng cách Manhattan** bắt đầu từ trang 2.

Để sửa báo cáo, mở `latex/main.tex` và các file `latex/sections/homework_*.tex` trong VS Code. LaTeX Workshop tự cập nhật `latex/build/main.pdf`. Bản `24120023.pdf` ở thư mục gốc là bản xuất để nộp; sau các lần sửa mới, cần xuất lại bản này từ PDF preview.
