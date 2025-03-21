from scoring import point_01,point_02,coin_04,coin_05,coin_06
def invited_text_generator(inviter_name,invitee_name,):
    text = f'''دستور_شروع_بولد{inviter_name}دستور_پایان_بولد عزیز! 
از همکاریت ممنونیم ❤️   دستور_شروع_بولد{invitee_name}دستور_پایان_بولد با دعوت تو به دستور_شروع_بولد «دانا پلاس شو» دستور_پایان_بولد پیوست 💥 
دستور_شروع_بولد{point_01} امتیازدستور_پایان_بولد پاداش دعوتت هم به موجودیت اضافه شد ✅'''
    return text

def review_comment_text_generator(user_name):
    text = f'''دستور_شروع_بولد{user_name}دستور_پایان_بولد عزیز!
از فعالیتت ممنونیم❤️ کامنت شما ثبت شد و الان در دست بررسیه‼
بعد از اینکه تائید بشه میتونی اونو ببینی🤩 همچنین دستور_شروع_بولد{coin_04} سکهدستور_پایان_بولد هم همون موقع به حسابت واریز میشه💸'''
    return text

def confirm_comment_text_generator(interaction):
    user_name = interaction.user.name
    book_name = interaction.book.name
    text = f'''دستور_شروع_بولد{user_name}دستور_پایان_بولد، نظر شما راجب کتاب دستور_شروع_بولد{book_name}دستور_پایان_بولد منتشر شد!
دستور_شروع_بولد{coin_04} سکهدستور_پایان_بولد هم به حسابت واریز شد'''
    return text
    
def reject_comment_text_generator(interaction):
    user_name = interaction.user.name
    book_name = interaction.book.name
    text = f'''دستور_شروع_بولد{user_name}دستور_پایان_بولد، متاسفانه نظر شما راجب کتاب دستور_شروع_بولد{book_name}دستور_پایان_بولد رد شد!'''
    return text

def review_activate_text_generator(user_name):
    text = f'''دستور_شروع_بولد{user_name}دستور_پایان_بولد عزیز!
به خاطر کوششت ازت ممنونیم❤️ کنش شما ثبت شد و الان در دست بررسیه‼
بعد از اینکه تائید بشه میتونی اونو ببینی🤩 همچنین دستور_شروع_بولد{point_02} امتیازدستور_پایان_بولد هم همون موقع به حسابت واریز میشه💰'''
    return text

def confirm_activate_text_generator(interaction):
    user_name = interaction.user.name
    author_name = interaction.book.name
    text = f'''دستور_شروع_بولد{user_name}دستور_پایان_بولد، کنش شما راجب کتاب دستور_شروع_بولد{author_name}دستور_پایان_بولد منتشر شد!
دستور_شروع_بولد{point_02} امتیازدستور_پایان_بولد هم به حسابت واریز شد'''
    return text
    
def reject_activate_text_generator(interaction):
    user_name = interaction.user.name
    book_name = interaction.book.name
    text = f'''دستور_شروع_بولد{user_name}دستور_پایان_بولد، متاسفانه کنش شما راجب کتاب دستور_شروع_بولد{book_name}دستور_پایان_بولد رد شد!'''
    return text

def camp_req_text_generator(user_name):
    text = f'''سلام امیدوارم حالتون خوب باشه!
من دستور_شروع_بولد{user_name}دستور_پایان_بولد هستم. خواستم بگم در اردوهای مدنظر شما شرکت کردم و واقعاً از این تجربه لذت بردم.
می‌خواستم بپرسم آیا امکانش هست که جایزه‌ام رو برام ارسال کنید؟'''
    return text

def course_req_text_generator(user_name):
    text = f'''سلام امیدوارم حالتون خوب باشه!
من، دستور_شروع_بولد{user_name}دستور_پایان_بولد، در دوره‌های تهیه شده شرکت کردم و واقعاً از تجربیات و محتوای آموزشی بهره‌ بردم.
خواستم بپرسم که آیا امکانش هست جایزه‌ای که برای حاضرین در نظر گرفته شده رو برام ارسال کنید؟ ممنون می‌شم اگر این درخواست رو بررسی کنید.'''
    return text

def confirm_camp_text_generator(user_name):
    text = f'''دستور_شروع_بولد{user_name}دستور_پایان_بولد! با در خواست تو مبتنی بر دریافت هدیه حضور در اردو موافقت شد
به همین دلیل دستور_شروع_بولد{coin_06} سکهدستور_پایان_بولد به حسابت واریز شد'''
    return text

def confirm_course_text_generator(user_name):
    text = f'''دستور_شروع_بولد{user_name}دستور_پایان_بولد! با در خواست تو مبتنی بر دریافت هدیه حضور در دوره ها موافقت شد
به همین دلیل دستور_شروع_بولد{coin_05} سکهدستور_پایان_بولد به حسابت واریز شد'''
    return text