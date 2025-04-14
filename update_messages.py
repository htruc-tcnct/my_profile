import google.generativeai as genai
import os
import json
from datetime import datetime

# --- Cấu hình ---
# Lấy API Key từ biến môi trường (sẽ được set bởi GitHub Actions)
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError("GEMINI_API_KEY không được thiết lập!")

genai.configure(api_key=API_KEY)

# Chọn model Gemini (ví dụ: gemini-1.5-flash)
model = genai.GenerativeModel('gemini-1.5-flash')

# Các chủ đề tương ứng với thẻ
CATEGORIES = ['coffee', 'love', 'inspiration', 'music']

# Tên file để lưu thông điệp
OUTPUT_FILE = "messages.json"

# --- Hàm tạo prompt ---
def create_prompt(category):
    """Tạo prompt cụ thể cho từng chủ đề."""
    theme = ""
    if category == 'coffee':
        theme = "Cà Phê và sự khởi đầu ngày mới"
    elif category == 'love':
        theme = "Tình Yêu và sự kết nối"
    elif category == 'inspiration':
        theme = "Cảm Hứng và động lực sống"
    elif category == 'music':
        theme = "Âm Nhạc và cảm xúc"
    else:
        theme = "cuộc sống" # Fallback

    # Prompt yêu cầu Gemini viết thông điệp
    # Thay đổi prompt nếu bạn muốn thông điệp theo phong cách khác
    return f"Viết một thông điệp ngắn gọn (khoảng 4-5 câu), vui vẻ, lạc quan và tích cực bằng tiếng Việt, liên quan đến chủ đề '{theme}'. Thông điệp này dành cho một người bất kỳ đọc vào buổi sáng để cảm thấy năng động, hào hứng và tràn đầy động lực cho ngày mới. Hãy khiến họ mỉm cười và bắt đầu ngày mới với tâm trạng tươi vui. Chỉ trả về nội dung thông điệp, không có lời chào hay giải thích thêm."


# --- Hàm gọi Gemini API ---
def get_gemini_message(prompt):
    """Gọi Gemini API và trả về nội dung text."""
    try:
        response = model.generate_content(prompt)
        # Kiểm tra xem có nội dung text trả về không
        if response.parts:
             # Trích xuất text, loại bỏ khoảng trắng thừa
            message = response.text.strip()
             # Đôi khi Gemini trả về trong markdown quote, loại bỏ nó
            if message.startswith('> '):
                message = message[2:].strip()
            if message.startswith('"') and message.endswith('"'):
                 message = message[1:-1].strip()

            # Đảm bảo không rỗng
            if message:
                return message
            else:
                 print(f"Warning: Gemini returned an empty message for prompt: {prompt}")
                 return "Hãy tự tạo thông điệp ý nghĩa cho ngày hôm nay của bạn nhé." # Fallback

        else:
            print(f"Warning: Gemini response did not contain parts for prompt: {prompt}")
            # Kiểm tra safety ratings nếu cần
            # print(response.prompt_feedback)
            return "Hôm nay vũ trụ muốn bạn tự mình khám phá thông điệp đặc biệt." # Fallback an toàn

    except Exception as e:
        print(f"Lỗi khi gọi Gemini API: {e}")
        # Trả về thông điệp lỗi hoặc mặc định
        return "Đã có lỗi xảy ra khi tạo thông điệp. Xin lỗi bạn."

# --- Main script ---
if __name__ == "__main__":
    print(f"Bắt đầu cập nhật thông điệp lúc: {datetime.now()}")
    daily_messages = {}

    for category in CATEGORIES:
        print(f"Đang lấy thông điệp cho chủ đề: {category}...")
        prompt = create_prompt(category)
        message = get_gemini_message(prompt)
        daily_messages[category] = message
        print(f"-> Thông điệp {category}: {message}")

    # Ghi dữ liệu vào file JSON
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(daily_messages, f, ensure_ascii=False, indent=4)
        print(f"Đã cập nhật thành công file {OUTPUT_FILE}")
    except Exception as e:
        print(f"Lỗi khi ghi file {OUTPUT_FILE}: {e}")

    print(f"Hoàn thành lúc: {datetime.now()}")