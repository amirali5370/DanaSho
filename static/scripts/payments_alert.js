{% with messages = get_flashed_messages() %}
    {% if messages %}
        {% for message in messages %}
            {% if message == "payment_success"%}
            swal({
                title: 'پرداخت موفقیت آمیز بود!',
                html: 'میتوانید از طریق پنل کاربری خود، مشخصات پرداخت را مشاهده فرمائید',
                type: 'success',
                confirmButtonColor: '#3f9b0b',
                confirmButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;"><i style="margin-left: 5px;" class="fa fa-times"></i> باشه</div>',
                showCloseButton: true,
                showLoaderOnConfirm:true,
                allowOutsideClick:false,
            }).then((result) => {swal.close();})
            {% elif message == "payment_failed" %}
            swal({
                title: 'پرداخت ناموفق!',
                html: "اگر وجه از حساب شما کم شده است، ظرف 72 ساعت آینده باز خواهد گشت.",
                type: 'error',
                confirmButtonColor: '#dc1225',
                confirmButtonText: '<div style="direction:rtl;font-size:18px;font-family:Iran,Calibri;font-weight:bold;"><i style="margin-left: 5px;" class="fa fa-times"></i> باشه</div>',
                showCloseButton: true,
                showLoaderOnConfirm:true,
                allowOutsideClick:false,
            }).then((result) => {swal.close();})
            {% endif %}
        {% endfor %}
    {% endif %}
{% endwith %}