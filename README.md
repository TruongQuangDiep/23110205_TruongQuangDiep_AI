# 1. Mục tiêu
Áp dụng được các thuật toán tìm kiếm trong bộ môn Trí tuệ nhân tạo vào bài toán 8 puzzle, giúp chúng ta có thể hiểu được nguyên lý hoạt động của các thuật toán dễ dàng hơn, cụ thể là biết được trạng thái đầu, trạng thái cuối, quá trình thực hiện, và không gian lưu trữ, độ phức tạp giải thuật. Qua đó, người học có thể so sánh và đánh giá mức độ tối ưu của các thuật toán.

# 2. Nội dung
- Không gian trạng thái: Tập hợp tất cả các trạng thái có thể đạt được từ trạng thái ban đầu bằng cách áp dụng các phép sinh (di chuyển lên, xuống, trái, phải trong 8 puzzle).  
- Trạng thái ban đầu (Initial State): Là trạng thái xuất phát của bài toán, trong bài toán này trạng thái ban đầu là ((2, 6, 5), (0, 8, 7), (4, 3, 1)).
- Trạng thái mục tiêu (Goal State): Là trạng thái mong muốn đạt được, trong bài toán này, trạng thái mong muốn đạt được là ((1, 2, 3), (4, 5, 6), (7, 8, 0)).
- Hàm sinh (Successor Function): Tạo ra các trạng thái kế tiếp từ 1 trạng thái hiện tại (di chuyển hợp lệ lên, xuống, trái, phải).
- Chi phí đường đi (Path Cost): Trong bài toán 8 puzzle này thì mỗi bước di chuyển là có thể coi chi phí là 1.
- Giải pháp (Solution): Là dãy các hành động (actions) hoặc trạng thái (states) từ trạng thái ban đầu đến trạng thái mục tiêu. Giải pháp có thể được đánh giá về độ dài (số bước), tổng chi phí và thời gian hoàn thành.
- Các tham số liên quan đến độ phức tạp:
+ b: Hệ số nhánh.
+ d: Độ sâu của lời giải.
+ m: Độ sâu tối đa của không gian trạng thái.

# 2.1. Các thuật toán tìm kiếm trong môi trường không có thông tin (Uninformed Search Algorithms)
- Định nghĩa: Thuật toán tìm kiếm không có thông tin (Uninformed Search Algorithms) là các thuật toán không sử dụng bất kì thông tin nào về khoảng cách tới đích hoặc vị trí của trạng thái đích.
- Chỉ dựa trên cấu trúc của không gian trạng thái và phép sinh kế tiếp

## Thuật toán BFS
- Ý tưởng: BFS tìm lời giải bằng cách duyệt các trạng thái theo từng lớp, đảm bảo tìm được đường đi ngắn nhất nếu tồn tại.
- Nguyên lý hoạt động: Thuật toán sử dụng hàng đợi (FIFO) để lần lượt mở rộng các trạng thái theo số bước tăng dần, tránh lặp bằng cách đánh dấu các trạng thái đã duyệt.
- Về đặc điểm:
+ Thời gian: O(b^d).
+ Không gian: O(b^d), vì phải lưu toàn bộ các nút cùng mức trong hàng đợi.
+ Tính đầy đủ: Có.
+ Tính tối ưu: Có.
+ Không gian trạng thái: Duyệt theo chiều rộng.
+ Nhược điểm: Tốn bộ nhớ vì phải lưu các trạng thái cùng mức.
![BFS](gif_files/BFS.gif)

## Thuật toán DFS
- Ý tưởng: DFS tìm lời giải bằng cách đi sâu vào nhánh hiện tại trước khi quay lại, khám phá trạng thái theo chiều sâu.
- Nguyên lý hoạt động: Thuật toán sử dụng ngăn xếp (LIFO) để lưu trữ và mở rộng trạng thái theo chiều sâu, đồng thời đánh dấu các trạng thái duyệt để tránh lặp.
- Về đặc điểm:
+ Thời gian: O(b^m).
+ Không gian: O(bm) , chỉ lưu tối đa một nhánh từ gốc đến lá.
+ Tính đầy đủ: Không, vì có thể đi vào vòng lặp nếu không giới hạn độ sâu.
+ Tính tối ưu: Không, vì lời giải chạy thuật toán này rất dài.
+ Không gian trạng thái: Duyệt theo chiều sâu.
+ Nhược điểm: Dễ bị mắc kẹt ở nhánh sai, không đảm bảo tìm được lời giải nếu không giới hạn độ sâu.
![DFS](gif_files/DFS.gif)

## Thuật toán UCS
- Ý tưởng: UCS tìm lời giải bằng cách luôn mở rộng trạng thái có chi phí đường đi nhỏ nhất từ trạng thái ban đầu.
- Nguyên lý hoạt động: Thuật toán sử dụng hàng đợi ưu tiên để lưu các trạng thái theo tổng chi phí từ đầu đến hiện tại, đảm bảo mở rộng nút có chi phí thấp nhất trước.
- Về đặc điểm: 
+ Thời gian: O(b^d)
+ Không gian: O(b^d)
+ Tính đầy đủ: Có (nếu tất cả bước đi có chi phí tương đương)
+ Tính tối ưu: Có (tìm được lời giải và chi phí lớn nhất)
+ Không gian trạng thái: Duyệt theo chi phí tăng dần.
+ Nhược điểm: Tốn bộ nhớ và thời gian nếu không gian trạng thái lớn.
![UCS](gif_files/UCS.gif)

# Thuật toán IDDFS
- Ý tưởng: Kết hợp ưu điểm của DFS (ít tốn bộ nhớ) và BFS (tìm được lời giải ngắn nhất) bằng cách lặp lại DFS với độ sâu tăng dần.
- Nguyên lý hoạt động: Thuật toán thực hiện tìm kiếm theo chiều sâu nhưng giới hạn độ sâu, sau đó tăng giới hạn dần lên và lặp lại cho đến khi tìm được lời giải. Trạng thái được kiểm tra lại nhiều lần ở các độ sâu khác nhau.
- Về đặc điểm: 
+ Thời gian: O(b^d), vì mỗi lớp độ sâu đều duyệt lại từ đầu.
+ Không gian: O(d), vì mỗi lần chỉ lưu đường đi hiện tại theo độ sâu.
+ Tính đầy đủ: Có (nếu độ sâu tăng đủ lớn và không gian trạng thái hữu hạn).
+ Tính tối ưu: Có (nếu chi phí các bước đi bằng nhau).
+ Không gian trạng thái: Duyệt theo chiều sâu, có kiểm soát.
+ Nhược điểm: Tốn thời gian vì phải lặp lại nhiều lần các bước đã duyệt ở độ sâu nhỏ hơn.
![IDDFS](gif_files/IDDFS.gif)

# 2.2. Các thuật toán tìm kiếm trong môi trường có thông tin (Informed Search Algorithms)
### Greedy Best-First Search
- Định nghĩa: Thuật toán tìm kiếm có thông tin (Informed Search Algorithms) là các thuật toán sử dụng thông tin bổ sung (heuristic) về khoảng cách hoặc ước lượng chi phí đến trạng thái đích để dẫn đường tìm kiếm.
- Mục tiêu: Giúp tăng hiệu quả tìm kiếm bằng cách ưu tiên mở rộng các trạng thái có khả năng dẫn đến đích nhanh hơn.

# Thuật toán A*
- Ý tưởng: A* kết hợp giữa chi phí thực từ điểm bắt đầu đến trạng thái hiện tại và chi phí ước lượng từ trạng thái hiện tại đến đích (sử dụng hàm heuristic) để chọn trạng thái mở rộng tiếp theo.
- Nguyên lý hoạt động: Thuật toán sử dụng hàng đợi ưu tiên (Priority Queue), trong đó mỗi trạng thái có tổng chi phí được tính theo công thức f(n) = g(n) + h(n)
+ g(n) là chi phí thực từ điểm bắt đầu đến trạng thái n
+ h(n) là hàm heuristic ước lượng chi phí từ n đến đích
+ Luôn mở rộng trạng thái có f(n) nhỏ nhất
- Về đặc điểm:
+ Thời gian: O(b^d)
+ Không gian: O(b^d), vì phải lưu toàn bộ trạng thái trong hàng đợi ưu tiên.
+ Tính đầy đủ: Có
+ Tính tối ưu: Có
+ Không gian trạng thái: Duyệt theo tổng chi phí ước lượng nhỏ nhất.
+ Nhược điểm: Tốn bộ nhớ và phụ thuộc vào chất lượng của hàm heuristic.
![AStar](gif_files/ASTAR.gif)

# Thuật toán IDA*
- Ý tưởng: IDA* kết hợp chiến lược lặp sâu dần (như IDDFS) với A* bằng cách sử dụng giới hạn f(n) = g(n) + h(n) và tăng giới hạn dần qua mỗi vòng lặp. Mục tiêu là tận dụng độ chính xác của A* mà vẫn tiết kiệm bộ nhớ.
- Nguyên lý hoạt động: Tính f(n) = g(n) + h(n) cho trạng thái ban đầu và đặt làm giới hạn (bound), thực hiện tìm kiếm theo chiều sâu nhưng chỉ duyệt các trạng thái có f(n) ≤ bound, nếu chưa có lời giải, cập nhật bound bằng f(n) nhỏ nhất vượt quá giới hạn trước. Lặp lại cho đến khi tìm thấy lời giải hoặc hết trạng thái.
- Về đặc điểm:
+ Thời gian: O(b^d), vì vẫn có thể duyệt lại các trạng thái nhiều lần như IDDFS.
+ Không gian: O(d), tiết kiệm bộ nhớ vì chỉ lưu đường đi hiện tại.
+ Tính đầy đủ: Có
+ Tính tối ưu: Có
+ Không gian trạng thái: Duyệt theo f(n) tăng dần, theo chiều sâu có kiểm soát.
+ Nhược điểm: Duyệt lặp lại nhiều, chậm nếu heuristic yếu, khó tận dụng bộ nhớ như A*.
![IDAStar](gif_files/IDASTAR.gif)

# 2.3. Các thuật toán tìm kiếm cục bộ (Local Search)
## Thuật toán Simple Hill Climbing (SHC)
- Ý tưởng: Luôn chọn và di chuyển sang trạng thái con đầu tiên có giá trị heuristic tốt hơn trạng thái hiện tại (tức nhỏ hơn), với mục tiêu tối ưu dần.
- Nguyên lý hoạt động: Bắt đầu từ trạng thái ban đầu, thuật toán thử các bước đi hợp lệ và chọn bước đầu tiên giúp giảm giá trị heuristic. Nếu không có bước nào cải thiện được, thuật toán dừng lại (mắc kẹt tại đỉnh cục bộ). 
- Về đặc điểm:
+ Thời gian: Có thể nhanh trong không gian nhỏ, nhưng dễ dừng sớm nếu gặp đỉnh cục bộ
+ Không gian: O(1) nếu không lưu lại các trạng thái, hoặc O(n) nếu lưu đường đi
+ Tính đầy đủ: Không (vì có thể dừng tại đỉnh cục bộ mà không đến đích)
+ Tính tối ưu: Không đảm bảo
+ Không gian trạng thái: Duyệt theo chiều sâu với kiểm tra cải thiện heuristic
![SHC](gif_files/SHC.gif)

## Thuật toán Steepest-ascent Hill Climbing (SAHC)
- Ý tưởng: Ở mỗi bước, thuật toán đánh giá tất cả các trạng thái con hợp lệ và chọn trạng thái có giá trị heuristic tốt nhất (nhỏ nhất) để di chuyển. Mục tiêu là tiến dần đến trạng thái đích bằng cách leo lên "dốc" nhanh nhất có thể.
-  Nguyên lý hoạt động: Bắt đầu từ trạng thái ban đầu, thuật toán thử tất cả bước đi hợp lệ. Với mỗi bước, nó tính giá trị heuristic của trạng thái mới. Nếu tồn tại một trạng thái con có heuristic tốt hơn hiện tại, thì chọn tốt nhất trong số đó để di chuyển. Nếu không tìm được trạng thái tốt hơn, thuật toán dừng lại (mắc kẹt tại cực trị cục bộ).
- Về đặc điểm:
+ Thời gian: Có thể nhanh nếu không gian trạng thái nhỏ và heuristic dẫn hướng tốt.
+ Không gian: O(n), lưu đường đi và các trạng thái đã duyệt.
+ Tính đầy đủ: Không đảm bảo (vì có thể mắc kẹt tại đỉnh cục bộ).
+ Tính tối ưu: Không (vì không xét toàn cục, chỉ quan tâm tốt nhất cục bộ).
+ Không gian trạng thái: Duyệt theo chiều sâu có đánh giá heuristic toàn bộ các con.
+ Nhược điểm: Dễ mắc kẹt tại cực trị cục bộ, không quay lui, phụ thuộc vào chất lượng heuristic và không đảm bảo tìm ra lời giải.
![SAHC](gif_files/SAHC.gif)

## Thuật toán Stochastic Hill Climbing (StoHC)
- Ý tưởng: Thay vì luôn chọn trạng thái con tốt nhất tuyệt đối, StoHC sẽ chọn ngẫu nhiên một trong các trạng thái con tốt hơn hiện tại, tránh bị mắc kẹt quá sớm tại đỉnh cục bộ.
- Nguyên lý hoạt động: Bắt đầu từ trạng thái hiện tại, thuật toán xét tất cả các bước đi hợp lệ. Với mỗi bước, tính giá trị heuristic của trạng thái mới. Nếu trạng thái mới có heuristic tốt hơn hiện tại, đưa vào danh sách các ứng viên. Sau đó, chọn ngẫu nhiên một trạng thái trong số đó để di chuyển. Nếu không có trạng thái nào tốt hơn, thuật toán dừng.
- Về đặc điểm: 
+ Thời gian: Phụ thuộc vào độ may rủi của quá trình chọn ngẫu nhiên; có thể nhanh nhưng cũng dễ kẹt.
+ Không gian: O(n), lưu trạng thái và đường đi.
+ Tính đầy đủ: Không đảm bảo (có thể mắc kẹt tại đỉnh cục bộ nếu không còn lựa chọn tốt hơn).
+ Tính tối ưu: Không đảm bảo (chọn ngẫu nhiên nên không luôn đạt trạng thái tốt nhất).
+ Không gian trạng thái: Duyệt theo chiều sâu nhưng có yếu tố ngẫu nhiên trong việc chọn bước.
+ Nhược điểm: Không quay lui, dễ mắc kẹt nếu không có cải thiện, phụ thuộc vào chất lượng heuristic và số lượng trạng thái tốt hơn tồn tại.
![StoHC](gif_files/StoHC.gif)

## Thuật toán Simulated Annealing (SA)
- Ý tưởng: Simulated Annealing mô phỏng quá trình làm nguội của kim loại. Ban đầu hệ thống có năng lượng cao (nhiệt độ cao), cho phép chấp nhận những bước đi "xấu hơn". Khi nhiệt độ giảm dần, hệ thống trở nên "kén chọn" hơn, hướng tới tối ưu cục bộ tốt hơn.
- Nguyên lý hoạt động: 
+ Khởi tạo trạng thái ban đầu và thiết lập nhiệt độ T lớn.
+ Trong khi T > min_temperature và chưa đạt đích:
	+ Xét các bước đi hợp lệ (lên, xuống, trái, phải).
	+ Nếu bước đi tạo trạng thái tốt hơn (heuristic giảm): luôn nhận.
	+ Nếu xấu hơn: chấp nhận với xác suất P = e^(-Δh / T) (Δh là hiệu số heuristic mới - cũ).
+ Sau mỗi lần duyệt, giảm nhiệt độ theo T *= cooling_rate.
+ Nếu không có bước đi nào được chấp nhận, thuật toán dừng.
- Về đặc điểm:
+ Thời gian: Phụ thuộc vào T, cooling_rate, độ sâu trạng thái và cấu trúc bài toán.
+ Không gian: O(n), lưu trạng thái hiện tại, visited và đường đi.
+ Tính đầy đủ: Không đảm bảo (có thể dừng sớm khi không có bước đi hợp lệ).
+ Tính tối ưu: Không đảm bảo, nhưng có khả năng thoát khỏi đỉnh cục bộ tốt hơn các thuật toán Hill Climbing khác.
+ Không gian trạng thái: Rất lớn - bao gồm tất cả các hoán vị hợp lệ của bài toán, SA không cần duyệt toàn bộ không gian, chỉ sinh ngẫu nhiên từng láng giềng trong quá trình "nguội”.
+ Nhược điểm: Không ổn định, kết quả khác nhau ở mỗi lần chạy, cần chỉnh tham số tốt (T, cooling_rate) để đạt hiệu quả cao, có thể không tìm ra nghiệm nếu làm nguội quá nhanh.
![SA](gif_files/SA.gif)

## Thuật toán Beam Search
- Ý tưởng: Beam Search là một thuật toán tìm kiếm heuristic tương tự như BFS nhưng giới hạn số lượng trạng thái mở rộng tại mỗi mức theo một tham số gọi là beam width. Điều này giúp giảm thiểu bộ nhớ và thời gian xử lý bằng cách chỉ giữ lại các trạng thái "tốt nhất" tại mỗi bước dựa trên hàm heuristic.
- Nguyên lý hoạt động: 
+ Bắt đầu từ trạng thái ban đầu.
+ Tại mỗi bước: Duyệt các trạng thái trong hàng đợi, sinh các trạng thái hợp lệ, đánh giá bằng heuristic, Chỉ giữ lại beam_width trạng thái có giá trị heuristic tốt nhất để tiếp tục mở rộng và trả về kết quả nếu tới trạng thái mục tiêu.
- Về đặc điểm:
+ Thời gian: Phụ thuộc vào beam_width, độ sâu của lời giải, và số lượng trạng thái hợp lệ mỗi bước.
+ Không gian: O(beam with * d), vì tại mỗi mức chỉ lưu tối đa beam_width trạng thái.	
+ Tính đầy đủ: Không đầy đủ nếu beam_width quá nhỏ - có thể bỏ qua nhánh chứa lời giải.
+ Tính tối ưu: Không tối ưu, vì thuật toán không đảm bảo chọn được đường đi ngắn nhất. Nó chỉ dựa vào giá trị heuristic cục bộ và có thể bỏ qua nhánh tốt hơn ở mức sâu hơn.
+ Không gian trạng thái: Rất lớn như trong các bài toán tổ hợp.
+ Nhược điểm: Dễ bỏ sót trạng thái nếu không nằm trong các nhánh được giữ lại.
![BeamSearch](gif_files/BeemSearch.gif)

## Thuật toán Genetic Algorithm
- Ở thuật toán này giao diện có hơi khác với các giao diện thuật toán ở trên, vì để mô phỏng dễ dàng và dễ hiểu hơn.
- Ý tưởng: Thuật toán di truyền mô phỏng quá trình tiến hóa tự nhiên, trong đó các cá thể (candidate solutions) được tạo ngẫu nhiên ban đầu, sau đó được chọn lọc, lai ghép và tiến hóa qua nhiều thế hệ để tìm ra cá thể tối ưu (có fitness tốt nhất). Trong bài toán này, mỗi cá thể đại diện cho một dãy hành động di chuyển từ trạng thái ban đầu, với mục tiêu tạo ra trạng thái khớp với trạng thái đích.
- Nguyên lý hoạt động: 
+ Tạo N cá thể (trong bài này N = 40), mỗi cá thể là chuỗi bước di chuyển ngẫu nhiên có độ dài cố định.
+ Đánh giá (Fitness Evaluation): Mỗi cá thể thực hiện chuỗi hành động từ trạng thái ban đầu. Nếu hợp lệ, tính fitness là tổng khoảng cách Manhattan đến trạng thái đích. Nếu gặp bước sai, cá thể bị loại.
+ Chọn lọc: Giữ lại các cá thể hợp lệ, sắp xếp theo fitness tăng dần và chọn ra số lượng cố định cá thể tốt nhất.
+ Lai tạo (Crossover): Tạo tất cả các cặp cha mẹ, lai bằng cách cắt chuỗi ở giữa và ghép phần của hai cá thể lại với nhau để tạo cá thể con.
+ Lặp lại: Tiếp tục lặp quá trình đánh giá → chọn lọc → lai tạo cho đến khi tìm được cá thể có fitness = 0 hoặc đạt số thế hệ tối đa.
+ Lưu kết quả: Sau mỗi thế hệ, ghi vào generation{số}.txt: số thế hệ, số cá thể hợp lệ, fitness tốt nhất và chuỗi hành động tương ứng.
- Về đặc điểm:
+ Thời gian: Phụ thuộc vào độ dài chuỗi hành động, số lượng cá thể và số thế hệ. Có thể chậm nếu chuỗi dài và lai tạo nhiều.
+ Không gian: O(n * m) với n là số cá thể và m là độ dài chuỗi hành động.
+ Tính đầy đủ: Không đầy đủ, vì không đảm bảo sinh ra cá thể tốt trong mọi lần chạy.
+ Tính tối ưu: Không đảm bảo tối ưu toàn cục, nhưng có khả năng tìm lời giải tốt hoặc chấp nhận được thông qua quá trình tiến hóa.
+ Không gian trạng thái: Rất lớn, nhưng Genetic Algorithm không cần duyệt toàn bộ. Thay vào đó, chỉ tiếp cận thông qua tiến hóa từng thế hệ.
+ Nhược điểm: Kết quả không ổn định, phụ thuộc vào quần thể ban đầu và quá trình lai tạo.
![GeneraticAlgorithm](gif_files/GeneraticAlgorithm.gif)

# 2.4. Các thuật toán tìm kiếm trong môi trường phức tạp (Search Algorithms in Complex Environments)
## Thuật toán And-Or Search
- Ý tưởng: Thuật toán And-Or Search là một thuật toán tìm kiếm đệ quy có cấu trúc nhánh "AND" và "OR", được sử dụng trong các bài toán có nhiều trạng thái và giải pháp có thể theo dạng cây phân nhánh. Thuật toán này tìm kiếm theo cách khác biệt so với các thuật toán tìm kiếm thông thường, nơi một số hành động phải được thực hiện cùng nhau (AND), trong khi các hành động khác có thể được thực hiện độc lập (OR).
- Nguyên lý hoạt động: Thuật toán And-Or Search khởi tạo trạng thái ban đầu và danh sách các trạng thái đã thăm. Tại mỗi bước, nếu trạng thái là mục tiêu, trả về chuỗi các bước dẫn đến mục tiêu. Nếu không, thử các hành động hợp lệ (AND hoặc OR), ưu tiên các trạng thái có khả năng đạt mục tiêu cao hơn
- Về đặc điểm: 
+ Thời gian: Thời gian tìm kiếm phụ thuộc vào kích thước không gian trạng thái và mức độ phân nhánh của bài toán.
+ Không gian: Tương tự như các thuật toán tìm kiếm đệ quy, thuật toán này cần lưu trữ các trạng thái đã thăm, do đó không gian có thể là O(n), với n là số trạng thái đã thăm trong quá trình tìm kiếm.
+ Tính đầy đủ: Không (thuật toán có thể không tìm được giải pháp)
+ Tính tối ưu: Không, nhưng có thể tìm được một giải pháp hợp lý trong không gian tìm kiếm.
+ Không gian trạng thái: Rất lớn, vì thuật toán phải tìm kiếm tất cả các trạng thái hợp lệ từ trạng thái ban đầu đến trạng thái mục tiêu.
+ Nhược điểm: Không ổn định, có thể trả về các kết quả khác nhau tùy vào thứ tự các hành động được thử nghiệm và các giá trị heuristic của các trạng thái nên không nhất quán.
![And_Or_Search](gif_files/And_Or_Search.gif)

## Thuật toán Belief State
- Ở thuật toán này giao diện có hơi khác với các giao diện thuật toán ở trên, nó bao gồm các thuật toán tìm kiếm bên trên, vì để mô phỏng dễ dàng và dễ hiểu hơn.
- Ý tưởng: Thuật toán Belief State được sử dụng trong môi trường không xác định, nơi trạng thái hiện tại không được biết chính xác. Thay vì một trạng thái cụ thể, thuật toán làm việc với một tập hợp các trạng thái khả dĩ (gọi là belief state). Mục tiêu là chuyển dần belief state về tập con chứa trạng thái mục tiêu.
- Nguyên lý hoạt động: Thuật toán khởi tạo belief state ban đầu, sau đó lặp lại quá trình áp dụng hành động lên tất cả các trạng thái để tạo ra belief state mới, loại bỏ các trạng thái không hợp lệ. Nếu belief state mới chứa mục tiêu, thuật toán trả về chuỗi hành động; ngược lại, tiếp tục tìm kiếm đến khi đạt mục tiêu hoặc không thể mở rộng thêm. 
- Về đặc điểm:
+ Thời gian: Phụ thuộc vào số lượng belief states có thể sinh ra và số hành động có thể thực hiện, và phụ thuộc vào thuật toán áp dụng vào.
+ Không gian: O(n), với n là số lượng belief states đã được duyệt.
+ Tính đầy đủ: Không đảm bảo.
+ Tính tối ưu: Không đảm bảo
+ Không gian trạng thái: Rất lớn.
+ Nhược điểm: Xử lý phức tạp hơn các thuật toán thông thường.
![Belief_State](gif_files/niemtinkocodauhieu_ok.gif)

## Thuật toán Search With Partial Observation
- Ý tưởng: Thuật toán này được thiết kế cho môi trường mà chỉ quan sát được một phần, biết được 1 phần của thông tin. Do đó, thuật toán cần kết hợp giữa thông tin quan sát được và mô hình hành động để suy đoán các trạng thái khả dĩ và chọn hành động phù hợp.
- Nguyên lý hoạt động: Thuật toán này cũng giống belief state nhưng khác ở chỗ là quan sát được 1 phần nên sau mỗi hành động và quan sát, sẽ loại bỏ những trạng thái mà không còn dấu hiệu đã cho ban đầu, thu hẹp và tiến gần đến mục tiêu hơn.
- Về đặc điểm:
+ Thời gian: Phụ thuộc vào độ lớn của không gian trạng thái và số lần quan sát cần thiết để thu hẹp belief state.
+ Không gian: Cần lưu trữ toàn bộ belief state ở mỗi bước, có thể lên đến O(n), với n là số trạng thái khả dĩ.
+ Tính đầy đủ: Không đảm bảo.
+ Tính tối ưu: Không đảm bảo.
+ Không gian trạng thái: Rất lớn.
+ Nhược điểm: Cần kết hợp chặt chẽ giữa suy luận và quan sát.
![Search_With_Partial_Observation](gif_files/Niemtincodauhieu_ok.gif)

# 2.5. Các thuật toán tìm kiếm trong môi trường có ràng buộc (Constraint Satisfaction Problems – CSPs)
## Thuật toán Generate-And-Test
- Ý tưởng: Thuật toán Generate-and-Test hoạt động bằng cách tạo ra tất cả (hoặc ngẫu nhiên một số) trạng thái ứng viên và kiểm tra xem chúng có thỏa mãn ràng buộc không.
- Ngữ cảnh áp dụng: Trong bài toán CSP 3x3, mỗi ô trong bảng là một biến, các giá trị cần gán là các số từ 0 đến 8, với ràng buộc: không có giá trị trùng lặp, 3 ô hàng giữa (1, 0), (1, 1), (1, 2) phải có giá trị cố định lần lượt là 4, 5, 6.
- Nguyên lý hoạt động: Thuật toán sinh ngẫu nhiên danh sách các giá trị từ 0 đến 8, sau đó duyệt qua tất cả các hoán vị có thể của danh sách này. Với mỗi hoán vị, ánh xạ các giá trị vào các ô trong bảng 3x3, rồi kiểm tra ràng buộc: tất cả giá trị phải khác nhau và ba ô ở hàng giữa phải lần lượt là 4, 5, 6. Nếu tìm được một hoán vị thỏa mãn, thuật toán dừng và trả về nghiệm, nếu không, trả về None.
- Về đặc điểm: 
+ Thời gian: Cực kỳ tốn thời gian nếu không gian trạng thái lớn - với 9 ô là 9! = 362880 hoán vị cần xét.
+ Không gian: Rất thấp - chỉ lưu hoán vị hiện tại và một vài log (O(1) đến O(n)).
+ Tính đầy đủ: Có - vì duyệt toàn bộ không gian nghiệm (nếu không dừng sớm).
+ Tính tối ưu: Không - dừng ngay khi tìm thấy nghiệm đầu tiên, không xét các nghiệm tốt hơn.
+ Không gian trạng thái: Rất lớn – n! với n là số biến cần gán.
+ Nhược điểm: Không hiệu quả với không gian trạng thái lớn.
![Generate_And_Test](gif_files/Kiemthu.gif)

## Thuật toán Backtracking
- Ý tưởng: Thuật toán Backtracking hoạt động bằng cách xây dựng lời giải dần dần, từng bước một. Tại mỗi bước, nó thử gán một giá trị vào biến chưa gán, sau đó kiểm tra ràng buộc. Nếu không vi phạm ràng buộc, tiếp tục gán biến tiếp theo. Nếu vi phạm, thuật toán quay lui (backtrack) để thử giá trị khác. Quá trình lặp lại cho đến khi tìm được nghiệm hoặc không còn lựa chọn nào.
- Ngữ cảnh: Trong bài toán CSP 3x3, mỗi ô trong bảng là một biến, các giá trị cần gán là các số từ 0 đến 8, với ràng buộc: tất cả giá trị trong bảng phải khác nhau, 3 ô hàng giữa (1,0), (1,1), (1,2) phải có giá trị cố định lần lượt là 4, 5, 6.
- Nguyên lý hoạt động: Thuật toán bắt đầu với bảng trống và gán giá trị cho từng ô chưa được gán. Tại mỗi bước, nó thử các giá trị từ 0 đến 8 theo thứ tự ngẫu nhiên. Nếu giá trị thỏa ràng buộc (khác nhau và đúng giá trị cố định), thuật toán gán và tiếp tục đệ quy. Nếu vi phạm, nó quay lui để thử giá trị khác. Khi tất cả ô được gán hợp lệ, thuật toán trả về nghiệm.
- Về đặc điểm: 
+ Thời gian: Cải thiện hơn so với Generate-and-Test nhờ loại bỏ sớm các nhánh sai (pruning), nhưng vẫn có thể chậm nếu không có chiến lược chọn biến/gán giá trị hiệu quả.
+ Không gian: Thấp – chỉ cần lưu trạng thái hiện tại (assignment) và ngăn xếp gọi đệ quy.
+ Tính đầy đủ: Có - sẽ tìm được nghiệm nếu tồn tại.
+ Tính tối ưu: Không - thuật toán dừng ở nghiệm đầu tiên thỏa mãn, không xét nghiệm tối ưu hơn.
+ Không gian trạng thái: Vẫn lớn – do duyệt các tổ hợp gán khác nhau, nhưng ít hơn nhiều so với duyệt toàn bộ hoán vị như Generate-and-Test.
+ Nhược điểm: Có thể vẫn chậm nếu không được tối ưu hóa.
![Backtracking](gif_files/Backtracking.gif)

## Thuật toán AC-3
- Ý tưởng: AC-3 (Arc Consistency Algorithm 3) là thuật toán kiểm tra và loại bỏ các giá trị không hợp lệ trong miền của các biến, đảm bảo rằng mọi giá trị còn lại đều thỏa mãn ràng buộc nhị phân với các biến liên quan.
- Ngữ cánh áp dụng: Trong bài toán CSP 3x3, mỗi ô là một biến với miền từ 0 đến 8, các ô giữa (1,0), (1,1), (1,2) có giá trị cố định là 4, 5, 6. Ràng buộc: tất cả các ô phải có giá trị khác nhau.
- Nguyên lý hoạt động: Thuật toán bắt đầu với hàng đợi chứa tất cả các cung ràng buộc giữa các biến. Với mỗi cung (Xi → Xj), thuật toán kiểm tra và loại bỏ giá trị khỏi miền của Xi nếu không còn giá trị nào trong miền của Xj thỏa mãn ràng buộc khác nhau. Nếu miền của Xi thay đổi, thuật toán đưa các cung liên quan đến Xi trở lại hàng đợi. Quá trình lặp lại cho đến khi hàng đợi rỗng hoặc có miền bị rỗng (không còn giá trị hợp lệ).
- Về đặc điểm: 
+ Thời gian: Nhanh hơn so với Generate-and-Test và Backtracking vì loại trừ sớm nhiều giá trị không cần thiết, nhưng vẫn phụ thuộc vào số lượng biến và ràng buộc.
+ Không gian: Trung bình - cần lưu miền của từng biến và hàng đợi các cung.
+ Tính đầy đủ: Có, đảm bảo các miền còn lại đều thỏa mãn tính nhất quán theo ràng buộc nhị phân
+ Tính tối ưu: Không, chỉ lọc miền chứ không tìm lời giải hoàn chỉnh.
+ Không gian trạng thái: Giảm nhiều nhờ thu hẹp miền giá trị trước khi tìm nghiệm.
+ Nhược điểm: Không giải bài toán hoàn chỉnh - chỉ là bước tiền xử lý hữu ích trước các thuật toán như Backtracking.
![AC-3](gif_files/AC3.gif)

# 2.6. Thuật toán học tăng cường (Reinforcement Learning)
## Thuật toán Q-Learning
- Ý tưởng: Q-learning là thuật toán học tăng cường giúp tối ưu hóa hành động trong môi trường bằng cách duy trì giá trị Q cho từng trạng thái và hành động, từ đó chọn hành động tốt nhất dựa trên việc học từ các quyết định trước đó.
- Ngữ cảnh: Bài toán 8-puzzle là bài toán trong đó bạn phải xếp lại các mảnh ghép của một bảng 3x3 sao cho chúng tạo thành một cấu trúc cố định (một trạng thái mục tiêu). Q-learning có thể giúp tìm ra chuỗi các bước di chuyển từ trạng thái ban đầu đến trạng thái mục tiêu.
- Nguyên lý hoạt động: 
+ Khởi tạo bảng Q: Mỗi trạng thái sẽ được lưu trữ với các giá trị của các hành động có thể thực hiện trong trạng thái đó.
+ Chọn hành động (epsilon-greedy): Trong mỗi bước, thuật toán sẽ chọn hành động theo chính sách epsilon-greedy, tức là có một xác suất epsilon để chọn hành động ngẫu nhiên và 1 - epsilon để chọn hành động có giá trị Q cao nhất.
+ Cập nhật giá trị Q: Sau khi thực hiện hành động và chuyển sang trạng thái mới, giá trị Q của trạng thái cũ được cập nhật dựa trên công thức:
Q(s,a)=Q(s,a)+α×(reward+γ×max a′Q(s′,a′)−Q(s,a))
- Trong đó:
+ α: Tốc độ học (learning rate).
+ γ: Hệ số giảm giá trị (discount factor).
+ reward: Phần thưởng nhận được khi thực hiện hành động.
+ maa′Q(s′,a′) Giá trị Q tối đa của trạng thái mới.
- Lặp lại: Thuật toán sẽ lặp lại quá trình này trong nhiều lần (episodes) cho đến khi đạt được trạng thái mục tiêu.
- Về đặc điểm:
+ Thời gian: Có thể chậm ban đầu vì cần khám phá nhiều trạng thái, nhưng sẽ nhanh hơn sau khi học được chính sách tốt.
+ Không gian: Cần lưu bảng Q có kích thước |S| x |A|, với |S| là số trạng thái có thể và |A| là số hành động, có thể rất lớn.
+ Tính đầy đủ: Có thể đạt được trạng thái mục tiêu nếu được huấn luyện đủ lâu và không gian trạng thái đủ bao phủ.
+ Tính tối ưu: Có thể đạt nghiệm tối ưu nếu được huấn luyện đủ lâu, nhưng phụ thuộc vào chính sách khám phá và tham số học.
+ Không gian trạng thái: Rất lớn.
+ Nhược điểm: Cần nhiều thời gian để học chính sách tốt nếu không có chiến lược khám phá hiệu quả, không hiệu quả nếu không gian trạng thái quá lớn (do bảng Q quá lớn)
![Q_Learning](gif_files/Q_Learning.gif)

# 3. Kết luận
- Đồ án này đã làm rõ được phần nào cách thức hoạt động và mô phỏng của các thuật toán tìm kiếm, để ta có thể biết được thuật toán nào có những ưu và nhược điểm riêng, độ phức tạp ra sao, để biết và áp dụng vào những bài toán khác nhau và phù hợp với mỗi thuật toán.
- Việc nắm vững kiến thức từng thuật toán trong này là vô cùng quan trọng, bởi không chỉ giúp chúng ta lựa chọn thuật toán phù hợp nhất mà còn bảo đảm hiệu quả và tối ưu trong việc giải quyết vấn đề. Trong quá trình thực hiện đồ án này, có rất nhiều khó khăn phải trải qua, nhưng cũng đã tìm cách và giải quyết khắc phục những khó khăn đó.
- Đồ án này không chỉ là tâm huyết của em mà cũng là sự cố gắng hết sức, nếu có sai xót hay chỗ nào còn chưa đúng thì đó cũng là một phần kinh nghiệm để giúp em hoàn thành tốt hơn nhưng đồ án sau.




