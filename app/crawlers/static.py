import requests
import time
from app.crawlers.base import BaseCrawler
from bs4 import BeautifulSoup
from app.redis_queue.queue import Queue
from urllib.parse import urljoin, urlparse

from app.url import normalize_url, get_robots_txt_disallowed_urls


class StaticCrawler(BaseCrawler):

    def __init__(self):
        self.disallow_urls = None
        self.queue = Queue('127.0.0.1', 6379)
        self.name=2

    def crawl(self,main_url,process_url_func):
        self.disallow_urls = get_robots_txt_disallowed_urls(main_url)

        while True:
            u = self.queue.pop_from_queue(self.name)
            if u is None:
                print('all urls done')
                break
            process_url_func(u)


            urls = self.derive_urls(u)
            for url in urls:
                self.queue.push_to_queue(self.name,url)
            # time.sleep(0.5)  # be polite


    def seed(self,main_url):

        urls = self.derive_urls(main_url)
        for url in urls:
            self.queue.push_to_queue(self.name,url)

    def derive_urls(self, url):

        base_domain = urlparse(url).netloc
        try:
            response = requests.get(url)
        except:
            return []

        if response.status_code==200:
            soup = BeautifulSoup(response.text, 'html.parser')

            hrefs = set()
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']

                if href.startswith('#'):
                    continue
                normalized_href = normalize_url(url, href)

                if urlparse(normalized_href).netloc == base_domain:
                    hrefs.add(normalized_href)
        else:
            return []
        return hrefs

#
# data = """  <!DOCTYPE html>
#     <html prefix="og: http://ogp.me/ns#" lang="fa">
#     <head>
#         <!-- Meta Tags -->
#         <meta charset="UTF-8"/>
#         <title>هتل بزرگ شیراز: رزرو هتل، لیست قیمت با تخفیف ویژه - هتل یار</title>
#         <meta name="description" content="رزرو هتل بزرگ شیراز در سایت هتل یار، مقایسه لیست قیمت اتاق ها و امکان کنسلی رایگان، آدرس و تلفن هتل + تضمین قیمت و نظرات کاربران | هتل یار"/>
#         <meta name="keywords" content="هتل،بزرگ،5 ستاره،رزرو،عکس"/>
#         <meta property="og:type" content="hotel"/>
#         <meta property="og:title" content="هتل بزرگ شیراز: رزرو هتل، لیست قیمت با تخفیف ویژه - هتل یار"/>
#         <meta property="og:description" content="رزرو هتل بزرگ شیراز در سایت هتل یار، مقایسه لیست قیمت اتاق ها و امکان کنسلی رایگان، آدرس و تلفن هتل + تضمین قیمت و نظرات کاربران | هتل یار"/>
#         <meta property="og:url" content="https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز"/>
#         <meta property="og:image" content="https://hotelyar.com/pic/726small.jpg"/>
#         <meta name="twitter:card" content="summary"/>
#         <meta name="twitter:site" content="@hotelyarbooking"/>
#         <meta name="twitter:title" content="هتل بزرگ شیراز: رزرو هتل، لیست قیمت با تخفیف ویژه - هتل یار"/>
#         <meta name="twitter:description" content="رزرو هتل بزرگ شیراز در سایت هتل یار، مقایسه لیست قیمت اتاق ها و امکان کنسلی رایگان، آدرس و تلفن هتل + تضمین قیمت و نظرات کاربران | هتل یار"/>
#         <meta name="twitter:url" content="https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز"/>
#         <meta name="twitter:image" content="https://hotelyar.com/pic/726small.jpg"/>
#         <!--<link rel="amphtml" href="/hotel/amp/726/هتل-بزرگ-شیراز">-->
#         <link rel="canonical" href="https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز"/>
#         <link rel="alternate" href="https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز" hreflang="x-default" />
#         <link rel="alternate" href="https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز" hreflang="fa" />
#         <link rel="alternate" href="https://en.hotelyar.com/hotel/726/grand--hotel-shiraz" hreflang="en" />
#             <!-- Meta Tags -->
#     <meta http-equiv="X-UA-Compatible" content="chrome=1">
#     <meta lang="fa"/>
#     <meta http-equiv="Content-Type" content="text/html" charset="UTF-8"/>
#     <meta name="viewport" content="width=device-width, initial-scale=1"/>
#     <meta name="description" content="https://hotelyar.com/"/>
#     <meta name="theme-color" content="#ad1f24">
#     <link rel="shortcut icon" type="image/x-icon" href="https://hotelyar.com/static/icons/icon_32.ico">
#     <!-- Shiv -->
#     <!--[if lte IE 9]
#     <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
#     <![endif]-->
#
#     <!-- Stylesheets -->
#     <link type="text/css" href="https://hotelyar.com/static/fonts/fonts.css" rel="stylesheet"/>
#     <link type="text/css" href="https://hotelyar.com/static/plugin/bootstrap-4.6.2/css/bootstrap-grid.min.css" rel="stylesheet"/>
#         <link type="text/css" href="https://hotelyar.com/static/plugin/OwlCarousel2-2.3.4/assets/owl.carousel.min.css" rel="stylesheet"/>
#     <link type="text/css" href="https://hotelyar.com/static/plugin/OwlCarousel2-2.3.4/assets/owl.theme.default.min.css" rel="stylesheet"/>
#             <link type="text/css" href="https://hotelyar.com/static/plugin/datepicker/css/datepicker.css" rel="stylesheet"/>
#
#     <link rel="manifest" href="manifest.json">
#
#     <!-- Main Stylesheet -->
#         <link type="text/css" href="https://hotelyar.com/static/css/style_main.css?rnd=253" rel="stylesheet"/>
#     <link type="text/css" href="https://hotelyar.com/static/css/style_main_additional.css?rnd=649" rel="stylesheet"/>
#         <script type="text/javascript" src="https://hotelyar.com/static/js/jquery-3.6.0.min.js"></script>
#
#     <!-- Google tag (gtag.js) -->
#     <script async src="https://www.googletagmanager.com/gtag/js?id=G-LBPG6W8TMX">
#     </script>
#     <script>
#
#         if ('serviceWorker' in navigator) {
#             navigator.serviceWorker.register('/service-worker.js')
#                 .then(function(registration) {
#                     console.log('Service Worker registered:', registration);
#                 }).catch(function(error) {
#                 console.error('Service Worker registration failed:', error);
#             });
#         }
#
#         window.dataLayer = window.dataLayer || [];
#         function gtag(){dataLayer.push(arguments);}
#         gtag('js', new Date());
#
#         gtag('config', 'G-LBPG6W8TMX');
#     </script>
#
#
#         <!-- Stylesheets -->
#         <link type="text/css" href="https://hotelyar.com/static/plugin/slick-1.8.1/css/slick.css" rel="stylesheet" />
#         <link type="text/css" href="https://hotelyar.com/static/plugin/slick-1.8.1/css/slick-theme.css" rel="stylesheet" />
#         <link type="text/css" href="https://hotelyar.com/static/plugin/lightgallery/css/lightgallery-bundle.min.css" rel="stylesheet" />
#         <!-- Main Stylesheet -->
#         <link type="text/css" href="https://hotelyar.com/static/css/style_hotel_single.css?rnd=358" rel="stylesheet" />
#         <link type="text/css" href="https://hotelyar.com/static/css/style_hotel_single_additional.css?rnd=309" rel="stylesheet" />
#
#
#                     <script>
#                 !function (t, e, n) {
#                     t.yektanetAnalyticsObject = n, t[n] = t[n] || function () {
#                         t[n].q.push(arguments)
#                     }, t[n].q = t[n].q || [];
#                     var a = new Date, r = a.getFullYear().toString() + "0" + a.getMonth() + "0" + a.getDate() + "0" + a.getHours(),
#                         c = e.getElementsByTagName("script")[0], s = e.createElement("script");
#                     s.id = "ua-script-q7ZdDMrw"; s.dataset.analyticsobject = n;
#                     s.async = 1; s.type = "text/javascript";
#                     s.src = "https://cdn.yektanet.com/rg_woebegone/scripts_v3/q7ZdDMrw/rg.complete.js?v=" + r, c.parentNode.insertBefore(s, c)
#                 }(window, document, "yektanet");
#             </script>
#             </head>
#     <body>
#     <!-- Start: Wait Book Form -->
#     <form action="/uiWaitBook.php" method="post" id="frmWaitBook">
#         <input type="hidden" name="hotelCode" value="726">
#         <input type="hidden" name="roomTypeCode">
#         <input type="hidden" name="fromDate" value="1403/11/14">
#         <input type="hidden" name="toDate" value="1403/11/15">
#     </form>
#     <!-- End: Wait Book Form -->
#
#     <!-- Start: Main Wrapper -->
#     <div class="ss-wrapper" >
#
#         <!-- Start: Main Header -->
#                 <header class="ss-header header-hotel-list">
#             <div class="ss-overlay"></div>
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12 header-mobile">
#                         <nav class="navbar bg-transparent navbar-expand-lg navbar-light" role="navigation">
#                             <a href="https://hotelyar.com" class="navbar-brand logo-main" aria-label="رزرو هتل">
#                                 <img src="https://hotelyar.com/static/img/theme/logo-main.svg" alt="">
#                             </a>
#                             <a href="https://hotelyar.com" class="navbar-brand logo-mobile" aria-label="رزرو هتل">
#                                 <img src="https://hotelyar.com/static/img/theme/logo-white.svg" alt="">
#                             </a>
#                             <div class="navbar-nav navbar-offcanvas navbar-offcanvas-touch justify-content-between bg-white flex-grow-1"
#                                  id="js-bootstrap-offcanvas">
#                                 <ul class="hn-menu">
#                                     <li><a href="https://hotelyar.com">رزرو هتل</a></li>
#                                     <li class="menu-item-has-children">
#                                         <span>
#                                             لیست هتل ها
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
#                                                     <path d="M192 384c-8.188 0-16.38-3.125-22.62-9.375l-160-160c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0L192 306.8l137.4-137.4c12.5-12.5 32.75-12.5 45.25 0s12.5 32.75 0 45.25l-160 160C208.4 380.9 200.2 384 192 384z"/>
#                                                 </svg>
#                                             </i>
#                                         </span>
#                                         <ul class="hn-dropdown-menu box-shadow">
#                                             <li><a href="/city/11/هتلهای-تهران">هتل های تهران</a></li><li><a href="/city/27/هتلهای-مشهد">هتل های مشهد</a></li><li><a href="/city/4/هتلهای-اصفهان">هتل های اصفهان</a></li><li><a href="/city/20/هتلهای-شیراز">هتل های شیراز</a></li><li><a href="/city/10/هتلهای-تبریز">هتل های تبریز</a></li><li><a href="/city/29/هتلهای-یزد">هتل های یزد</a></li><li><a href="/city/23/هتلهای-کیش">هتل های کیش</a></li><li><a href="/city/112/هتلهای-رشت">هتل های رشت</a></li><li><a href="https://hotelyar.com/لیست-هتل-های-ایران">لیست همه شهرها</a></li>                                        </ul>
#                                     </li>
#                                     <li class="menu-item-has-children">
#                                         <span>
#                                             بهترین هتل ها
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
#                                                     <path d="M192 384c-8.188 0-16.38-3.125-22.62-9.375l-160-160c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0L192 306.8l137.4-137.4c12.5-12.5 32.75-12.5 45.25 0s12.5 32.75 0 45.25l-160 160C208.4 380.9 200.2 384 192 384z"/>
#                                                 </svg>
#                                             </i>
#                                         </span>
#                                         <ul class="hn-dropdown-menu box-shadow">
#                                             <li><a href="/بهترین-هتلهای-ایران" rel="follow"  >بهترین هتل های  ایران</a></li><li><a href="/بهترین-هتلهای-تهران" rel="follow"  >بهترین هتل های  تهران</a></li><li><a href="/بهترین-هتلهای-کیش" rel="follow"  >بهترین هتل های  کیش</a></li><li><a href="/بهترین-هتلهای-مشهد" rel="follow"  >بهترین هتل های  مشهد</a></li><li><a href="/بهترین-هتلهای-شیراز" rel="follow"  >بهترین هتل های  شیراز</a></li><li><a href="/بهترین-هتلهای-تبریز" rel="follow"  >بهترین هتل های  تبریز</a></li><li><a href="/بهترین-هتلهای-اصفهان" rel="follow"  >بهترین هتل های  اصفهان</a></li><li><a href="/بهترین-هتلهای-یزد" rel="follow"  >بهترین هتل های  یزد</a></li><li><a href="/بهترین-هتلهای-رامسر" rel="follow"  >بهترین هتل های  رامسر</a></li><li><a href="/بهترین-هتلهای-رشت" rel="follow"  >بهترین هتل های  رشت</a></li>                                        </ul>
#                                     </li>
#                                                                             <li class="hn-menu-link-mobile d-none" id="airport-register">
#                                             <a href="https://hotelyar.com/airport-register">ثبت نام فرودگاه</a>
#                                         </li>
#
#                                     <li class="hn-menu-track">
#                                         <a class="color-red" href="https://hotelyar.com/uiTracking.php" rel="follow" >
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512">
#                                                     <path d="M576 208C549.5 208 528 229.5 528 256C528 282.5 549.5 304 576 304V384C576 419.3 547.3 448 512 448H64C28.65 448 0 419.3 0 384V304C26.51 304 48 282.5 48 256C48 229.5 26.51 208 0 208V128C0 92.65 28.65 64 64 64H512C547.3 64 576 92.65 576 128V208zM64 112C55.16 112 48 119.2 48 128V172.8C76.69 189.4 96 220.5 96 256C96 291.5 76.69 322.6 48 339.2V384C48 392.8 55.16 400 64 400H512C520.8 400 528 392.8 528 384V339.2C499.3 322.6 480 291.5 480 256C480 220.5 499.3 189.4 528 172.8V128C528 119.2 520.8 112 512 112H64z"/>
#                                                 </svg>
#                                             </i>پیگیری رزرو
#                                         </a>
#                                     </li>
#
#
# <!--                                    <li class="hn-menu-track">
#                                         <a class="color-red" href="https://hotelyar.com/sapay.php" rel="follow" >
#                                             <i>
#                                             </i>پرداخت آنلاین
#                                         </a>
#                                     </li>-->
#
#                                     <li class="hn-menu-link-mobile">
#                                         <a href="https://hotelyar.com/راهنما">معرفی هتل یار</a>
#                                     </li>
#                                     <li class="hn-menu-link-mobile">
#                                         <a href="https://hotelyar.com/privacy.php">Privacy Policy</a>
#                                     </li>
#                                 </ul>
#                                 <div class="hn-links">
#                                     <a class="hn-links-item bg-light h-nav-language box-hover-red hn-menu-lang-mobile"
#                                        href="https://en.hotelyar.com/">
#                                         <span class="color-gray">Language:</span> EN
#                                     </a>
#                                     <a class="hn-links-item ss-btn-red h-nav-login"
#                                        href="https://hotelyar.com/memberPanel.php">
#                                         <i>
#                                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"
#                                                  class="rotate">
#                                                 <path d="M512 128v256c0 53.02-42.98 96-96 96h-72C330.7 480 320 469.3 320 456c0-13.26 10.75-24 24-24H416c26.4 0 48-21.6 48-48V128c0-26.4-21.6-48-48-48h-72C330.7 80 320 69.25 320 56C320 42.74 330.7 32 344 32H416C469 32 512 74.98 512 128zM345.5 239.6l-128-136C208.4 93.88 193.2 93.44 183.6 102.5C173.9 111.6 173.4 126.8 182.5 136.4L272.4 232H24C10.75 232 0 242.8 0 256s10.75 24 24 24h248.4l-89.92 95.56c-9.094 9.656-8.625 24.84 1.031 33.91C188.2 413.8 194.1 416 200 416c6.375 0 12.75-2.531 17.47-7.562l128-136C354.2 263.2 354.2 248.8 345.5 239.6z"/>
#                                             </svg>
#                                         </i>
#                                         <span>حساب کاربری</span>
#                                     </a>
#                                     <div class="hn-links-item h-nav-date-social">
#                                         <span class="h-nav-ds-date color-gray">یک‌شنبه ۱۴ بهمن ۱۴۰۳</span>
#                                         <div class="h-nav-ds-social">
#                                             <a href="https://t.me/Hotelyar84" target="_blank" aria-label="کانال رسمی هتل یار در تلگرام" rel="nofollow">
#                                                 <i>
#                                                     <svg fill="#000000" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 25 25">
#                                                         <path d="M12.5,0C5.6,0,0,5.6,0,12.5S5.6,25,12.5,25S25,19.4,25,12.5S19.4,0,12.5,0z M12.5,1.2c6.2,0,11.3,5.1,11.3,11.3
#                                                                                 s-5.1,11.3-11.3,11.3S1.2,18.7,1.2,12.5S6.3,1.2,12.5,1.2z M17.6,7.6c-0.3,0-0.7,0-1.1,0.2C15.8,8,6.4,12.1,5.8,12.3
#                                                                                 c-0.5,0.2-1,0.5-1,0.8c0,0.2,0.1,0.4,0.5,0.5s1.5,0.5,2.1,0.6c0.6,0.2,1.3,0,1.7-0.2c0.4-0.3,5.1-3.4,5.4-3.6
#                                                                                 c0.3-0.3,0.6,0.1,0.3,0.4c-0.3,0.3-3.5,3.4-3.9,3.8c-0.5,0.5-0.1,1.1,0.2,1.3c0.4,0.2,3.2,2.1,3.6,2.4s0.9,0.4,1.2,0.4
#                                                                                 s0.6-0.5,0.8-1.1c0.2-0.7,1.3-7.7,1.4-9.1C18.1,8.1,18,7.8,17.6,7.6C17.8,7.6,17.7,7.6,17.6,7.6z"/>
#                                                     </svg>
#                                                 </i>
#                                             </a>
#                                             <a href="https://instagram.com/hotelyar" target="_blank" aria-label="پیج رسمی هتل یار در اینستاگرام" rel="nofollow">
#                                                 <i>
#                                                     <svg fill="#000000" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">
#                                                         <path d="M8.3,0C3.7,0,0,3.7,0,8.3v11.5C0,24.3,3.7,28,8.3,28h11.5c4.6,0,8.3-3.7,8.3-8.3V8.3C28,3.7,24.3,0,19.7,0H8.3z M8.4,1.6
#                                                                                 h11.2c3.8,0,6.8,3.1,6.8,6.8v11.2c0,3.8-3.1,6.8-6.8,6.8H8.4c-3.8,0-6.8-3.1-6.8-6.8V8.4C1.6,4.6,4.6,1.6,8.4,1.6z M21.6,5.1
#                                                                                 c-0.7,0-1.3,0.6-1.3,1.3s0.6,1.3,1.3,1.3s1.3-0.6,1.3-1.3S22.3,5.1,21.6,5.1z M14,7c-3.9,0-7,3.1-7,7s3.1,7,7,7s7-3.1,7-7
#                                                                                 S17.9,7,14,7z M14,8.6c3,0,5.4,2.4,5.4,5.4S17,19.4,14,19.4S8.6,17,8.6,14S11,8.6,14,8.6z"/>
#                                                     </svg>
#                                                 </i>
#                                             </a>
#                                         </div>
#                                     </div>
#                                 </div>
#                             </div>
#                         </nav>
#                         <div class="hn-mobile-icons">
#                             <button class="navbar-toggler offcanvas-toggle" type="button" data-toggle="offcanvas"
#                                     data-target="#js-bootstrap-offcanvas" aria-controls="navbarTogglerDemo03"
#                                     aria-expanded="false" aria-label="Toggle navigation">
#                                 <a class="navbar-toggler-link white">
#                                     <span></span>
#                                     <span></span>
#                                     <span></span>
#                                 </a>
#                             </button>
#                             <a href="https://hotelyar.com/memberPanel.php">
#                                 <i>
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="rotate">
#                                         <path d="M352 256c0-4.094-1.562-8.188-4.688-11.31l-144-144c-6.25-6.25-16.38-6.25-22.62 0s-6.25 16.38 0 22.62L297.4 240H16C7.156 240 0 247.2 0 256s7.156 16 16 16h281.4l-116.7 116.7c-6.25 6.25-6.25 16.38 0 22.62s16.38 6.25 22.62 0l144-144C350.4 264.2 352 260.1 352 256zM432 32h-96C327.2 32 320 39.16 320 48S327.2 64 336 64h96C458.5 64 480 85.53 480 112v288c0 26.47-21.53 48-48 48h-96c-8.844 0-16 7.156-16 16s7.156 16 16 16h96c44.13 0 80-35.88 80-80v-288C512 67.88 476.1 32 432 32z"/>
#                                     </svg>
#                                 </i>
#                             </a>
# <!--                            <a href="https://t.me/Hotelyar84" target="_blank" rel="nofollow">
#                                 <i>
#                                     <svg fill="#000000" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 25 25">
#                                         <path d="M12.5,0C5.6,0,0,5.6,0,12.5S5.6,25,12.5,25S25,19.4,25,12.5S19.4,0,12.5,0z M12.5,1.2c6.2,0,11.3,5.1,11.3,11.3
#                                                                                 s-5.1,11.3-11.3,11.3S1.2,18.7,1.2,12.5S6.3,1.2,12.5,1.2z M17.6,7.6c-0.3,0-0.7,0-1.1,0.2C15.8,8,6.4,12.1,5.8,12.3
#                                                                                 c-0.5,0.2-1,0.5-1,0.8c0,0.2,0.1,0.4,0.5,0.5s1.5,0.5,2.1,0.6c0.6,0.2,1.3,0,1.7-0.2c0.4-0.3,5.1-3.4,5.4-3.6
#                                                                                 c0.3-0.3,0.6,0.1,0.3,0.4c-0.3,0.3-3.5,3.4-3.9,3.8c-0.5,0.5-0.1,1.1,0.2,1.3c0.4,0.2,3.2,2.1,3.6,2.4s0.9,0.4,1.2,0.4
#                                                                                 s0.6-0.5,0.8-1.1c0.2-0.7,1.3-7.7,1.4-9.1C18.1,8.1,18,7.8,17.6,7.6C17.8,7.6,17.7,7.6,17.6,7.6z"/>
#                                     </svg>
#                                 </i>
#                             </a>-->
#
#
#                             <a href="https://instagram.com/hotelyar" target="_blank" rel="nofollow">
#                                 <i>
#                                     <svg fill="#000000" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28">
#                                         <path d="M8.3,0C3.7,0,0,3.7,0,8.3v11.5C0,24.3,3.7,28,8.3,28h11.5c4.6,0,8.3-3.7,8.3-8.3V8.3C28,3.7,24.3,0,19.7,0H8.3z M8.4,1.6
#                                                                                 h11.2c3.8,0,6.8,3.1,6.8,6.8v11.2c0,3.8-3.1,6.8-6.8,6.8H8.4c-3.8,0-6.8-3.1-6.8-6.8V8.4C1.6,4.6,4.6,1.6,8.4,1.6z M21.6,5.1
#                                                                                 c-0.7,0-1.3,0.6-1.3,1.3s0.6,1.3,1.3,1.3s1.3-0.6,1.3-1.3S22.3,5.1,21.6,5.1z M14,7c-3.9,0-7,3.1-7,7s3.1,7,7,7s7-3.1,7-7
#                                                                                 S17.9,7,14,7z M14,8.6c3,0,5.4,2.4,5.4,5.4S17,19.4,14,19.4S8.6,17,8.6,14S11,8.6,14,8.6z"/>
#                                     </svg>
#                                 </i>
#                             </a>
#
#                                                             <a href="/mobileapp">
#                                     <i>
#                                         <svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor"><path d="M19.5 19.125a.75.75 0 0 1 .087 1.495l-.087.005h-15a.75.75 0 0 1-.087-1.495l.087-.005h15ZM12 3.375a.75.75 0 0 1 .745.663l.005.087v9.815l3.797-3.797a.75.75 0 0 1 .99-.063l.07.063a.75.75 0 0 1 .063.99l-.063.07-5.077 5.077a.725.725 0 0 1-.064.057l.065-.056a.756.756 0 0 1-.102.085l-.033.021a.533.533 0 0 1-.048.028l-.026.013a.547.547 0 0 1-.054.023l-.023.008a.57.57 0 0 1-.057.018l-.034.007a.505.505 0 0 1-.09.013.52.52 0 0 1-.039.003h-.049a.854.854 0 0 1-.04-.002L12 16.5a.754.754 0 0 1-.537-.226l-5.07-5.07a.75.75 0 0 1 .99-1.124l.07.063 3.797 3.796V4.126a.75.75 0 0 1 .75-.75Z" fill-rule="evenodd"></path></svg>
#                                     </i>
#                                 </a>
#                                                     </div>
#                     </div>
#                 </div>
#             </div>
#         </header>
#                 <!-- Ends: Main Header -->
#         <!-- Start: breadcrumb -->
#         <div class="ss-hotel-single-breadcrumb-container">
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12">
#                         <div class="ss-hotel-single-breadcrumb-wrapper">
#                             <div class="ss-hotel-single-bw-breadcrumb">
#                                 <ol itemscope itemtype="https://schema.org/BreadcrumbList" class="ss-breadcrumb">
#                                     <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
#                                         <a itemprop="item" href="https://hotelyar.com"><span itemprop="name">صفحه نخست</span></a>
#                                         <meta itemprop="position" content="1">
#                                     </li>
#                                     <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
#                                         <a itemprop="item" href="https://hotelyar.com/city/20/هتلهای-شیراز"><span itemprop="name">هتل های شیراز</span></a>
#                                         <meta itemprop="position" content="2">
#                                     </li>
#                                     <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
#                                         <span itemprop="name">هتل بزرگ شیراز</span>
#                                         <meta itemprop="position" content="3">
#                                     </li>
#                                 </ol>
#                             </div>
#                             <div class="ss-hotel-single-bw-link ">
#                                 <a href="https://hotelyar.com/city/20/هتلهای-شیراز">هتل های
#                                     <span>شیراز</span>
#                                     <i>
#                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path>
#                                         </svg>
#                                     </i>
#                                 </a>
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         </div>
#         <!-- Ends: breadcrumb -->
#         <!-- Start: gallery -->
#         <section class="ss-inner-main">
#             <div class="ss-inner-main-bg"></div>
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12">
#                         <div class="ss-hotel-single-head">
#                             <div class="ss-hotel-single-head-content">
#                                 <div class="ss-hotel-single-h-header-wrapper">
#                                     <div class="ss-hotel-single-hhw-title">
#                                         <h1 class="ss-hotel-single-hhwt-name">هتل بزرگ شیراز</h1>
#                                                                                     <div class="stars-wrapper stars-large ss-hotel-single-hhwt-stars">
#                                                 <div aria-hidden="true" focusable="false" class="stars"><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span></div>
#                     <span class="stars-title color-gray">(پنج ستاره)</span>                                            </div>
#                                                                             </div>
#                                                                             <div class="ss-hotel-single-hhw-meta">
#                                             <div class="ss-hotel-single-hhwm-suggest ss-hotel-single-hhwm-item">توصیه شده توسط<span>100%</span>  مسافران
#                                             </div>
#                                         </div>
#                                                                     </div>
#                                 <div class="ss-hotel-single-h-header-location">
#                                     <i>
#                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M272 192C272 236.2 236.2 272 192 272C147.8 272 112 236.2 112 192C112 147.8 147.8 112 192 112C236.2 112 272 147.8 272 192zM192 160C174.3 160 160 174.3 160 192C160 209.7 174.3 224 192 224C209.7 224 224 209.7 224 192C224 174.3 209.7 160 192 160zM384 192C384 279.4 267 435 215.7 499.2C203.4 514.5 180.6 514.5 168.3 499.2C116.1 435 0 279.4 0 192C0 85.96 85.96 0 192 0C298 0 384 85.96 384 192H384zM192 48C112.5 48 48 112.5 48 192C48 204.4 52.49 223.6 63.3 249.2C73.78 274 88.66 301.4 105.8 329.1C134.2 375.3 167.2 419.1 192 451.7C216.8 419.1 249.8 375.3 278.2 329.1C295.3 301.4 310.2 274 320.7 249.2C331.5 223.6 336 204.4 336 192C336 112.5 271.5 48 192 48V48z"></path>
#                                         </svg>
#                                     </i>
#
#                                     <div class="color-gray">
#                                     <span>
#                                         آدرس هتل: شیراز - دروازه قرآن                                    </span>
#                                     </div>
#                                 </div>
#                                 <div class="ss-hotel-single-h-header-features">
#                                     <div class="ss-hotel-single-h-header-features-item">
#                                                                                     <div class="ss-hotel-single-hhfi-icon">
#                                                 <i>
#                                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 101L294.8 38.97C309.9 14.73 336.5 0 365.1 0H368C412.2 0 448 35.82 448 80C448 98.01 442 114.6 432 128H464C490.5 128 512 149.5 512 176V240C512 260.9 498.6 278.7 480 285.3V448C480 483.3 451.3 512 416 512H96C60.65 512 32 483.3 32 448V285.3C13.36 278.7 0 260.9 0 240V176C0 149.5 21.49 128 48 128H79.99C69.95 114.6 64 98.01 64 80C64 35.82 99.82 0 144 0H146.9C175.5 0 202.1 14.73 217.2 38.97L256 101zM365.1 32C347.5 32 331.2 41.04 321.9 55.93L276.9 128H368C394.5 128 416 106.5 416 80C416 53.49 394.5 32 368 32H365.1zM235.1 128L190.1 55.93C180.8 41.04 164.5 32 146.9 32H144C117.5 32 96 53.49 96 80C96 106.5 117.5 128 144 128H235.1zM48 160C39.16 160 32 167.2 32 176V240C32 248.8 39.16 256 48 256H240V160H48zM272 256H464C472.8 256 480 248.8 480 240V176C480 167.2 472.8 160 464 160H272V256zM240 288H64V448C64 465.7 78.33 480 96 480H240V288zM272 480H416C433.7 480 448 465.7 448 448V288H272V480z"/>
#                                                     </svg>
#                                                 </i>
#                                             </div>
#                                             <div class="ss-hotel-single-hhfi-content">
#                                                 <span class="ss-hotel-single-hhfic-title color-gray">امتیاز تا</span>
#                                                 <span class="ss-hotel-single-hhfic-val">161</span>
#                                             </div>
#                                                                             </div>
#                                     <div class="ss-hotel-single-h-header-features-item">
#                                         <div class="ss-hotel-single-hhfi-icon">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M80 296C80 282.7 90.75 272 104 272C117.3 272 128 282.7 128 296C128 309.3 117.3 320 104 320C90.75 320 80 309.3 80 296zM432 296C432 309.3 421.3 320 408 320C394.7 320 384 309.3 384 296C384 282.7 394.7 272 408 272C421.3 272 432 282.7 432 296zM48.29 204.7L82.99 89.01C93.14 55.17 124.3 32 159.6 32H352.4C387.7 32 418.9 55.17 429 89.01L463.7 204.7C492.6 221.2 512 252.3 512 288V464C512 472.8 504.8 480 496 480C487.2 480 480 472.8 480 464V416H32V464C32 472.8 24.84 480 16 480C7.164 480 0 472.8 0 464V288C0 252.3 19.44 221.2 48.29 204.7zM85.33 192.6C88.83 192.2 92.39 192 96 192H416C419.6 192 423.2 192.2 426.7 192.6L398.4 98.21C392.3 77.9 373.6 64 352.4 64H159.6C138.4 64 119.7 77.9 113.6 98.21L85.33 192.6zM32 288V384H480V288C480 260.3 462.4 236.7 437.7 227.8L437.3 227.9L437.2 227.6C430.5 225.3 423.4 224 416 224H96C88.58 224 81.46 225.3 74.83 227.6L74.73 227.9L74.27 227.8C49.62 236.7 32 260.3 32 288V288z"/></svg>
#                                             </i>
#                                         </div>
#
#                                         <div class="ss-hotel-single-hhfi-content">
#                                             <span class="ss-hotel-single-hhfic-title color-gray">اجاره خودرو </span>
#                                             <span class="ss-hotel-single-hhfic-val">
#                                                                                             <i>
#                                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path d="M312.1 375c9.369 9.369 9.369 24.57 0 33.94s-24.57 9.369-33.94 0L160 289.9l-119 119c-9.369 9.369-24.57 9.369-33.94 0s-9.369-24.57 0-33.94L126.1 256L7.027 136.1c-9.369-9.369-9.369-24.57 0-33.94s24.57-9.369 33.94 0L160 222.1l119-119c9.369-9.369 24.57-9.369 33.94 0s9.369 24.57 0 33.94L193.9 256L312.1 375z"/></svg>
#                                                 </i>
#                                                                                                                                 </span>
#                                         </div>
#                                     </div>
#                                                                             <div class="ss-hotel-single-h-header-features-item">
#                                             <div class="ss-hotel-single-hhfi-icon">
#                                                 <i>
#                                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M232 224c-13.25 0-24 14.33-24 31.1S218.7 288 232 288S256 273.7 256 256S245.3 224 232 224zM260.4 1.443l-160 40C78.1 46.79 64 65.1 64 88.03V480H16C7.164 480 0 487.2 0 496C0 504.8 7.164 512 16 512H288c17.67 0 32-14.33 32-32V49.15c0-10.14-2.611-20.34-8.523-28.59C299.4 3.707 279.3-3.279 260.4 1.443zM288 480H96V88.04c0-7.373 5-13.75 12.12-15.53l160-40C272.9 31.22 277.9 32.38 281.8 35.41C285.8 38.47 288 43.07 288 48.04V480zM560 480H512V144c0-44.18-35.82-79.1-79.1-79.1H368c-8.836 0-16 7.162-16 15.1s7.164 16 16 16h64c26.51 0 48 21.49 48 48V480c0 17.67 14.33 32 32 32h48c8.836 0 16-7.164 16-15.1C576 487.2 568.8 480 560 480z"/></svg>
#                                                 </i>
#                                             </div>
#                                             <div class="ss-hotel-single-hhfi-content">
#                                                 <span class="ss-hotel-single-hhfic-title color-gray">تعداد اتاق </span>
#                                                 <span class="ss-hotel-single-hhfic-val">158</span>
#                                             </div>
#                                         </div>
#                                                                             <div class="ss-hotel-single-h-header-features-item">
#                                             <div class="ss-hotel-single-hhfi-icon">
#                                                 <i>
#                                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M576 48C576 56.84 568.8 64 560 64H448v112C448 184.8 440.8 192 432 192h-128v144c0 8.844-7.156 16-16 16H160v112C160 472.8 152.8 480 144 480h-128C7.156 480 0 472.8 0 464S7.156 448 16 448H128v-112C128 327.2 135.2 320 144 320h128V176C272 167.2 279.2 160 288 160h128V48C416 39.16 423.2 32 432 32h128C568.8 32 576 39.16 576 48z"/>
#                                                     </svg>
#                                                 </i>
#                                             </div>
#                                             <div class="ss-hotel-single-hhfi-content">
#                                                 <span class="ss-hotel-single-hhfic-title color-gray">تعداد طبقه  </span>
#                                                 <span class="ss-hotel-single-hhfic-val">14</span>
#                                             </div>
#                                         </div>
#                                                                     </div>
#                             </div>
#                                                                                             <div class="ss-hotel-single-head-map">
#
#                                     <a href="https://maps.google.com/?q=29.634857,52.560072(هتل بزرگ شیراز)" class="ss-hotel-single-hm-map item-hover" style="background-image: url(https://hotelyar.com/static/img/theme/hotel-list-map-bg-01.jpg);" target="_blank">
#                                         <div class="ss-hotel-single-hmm-box">
#                                             مسیریاب هتل بزرگ شیراز                                        </div>
#                                         <i>
#                                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M168.3 499.2C116.1 435 0 279.4 0 192C0 85.96 85.96 0 192 0C298 0 384 85.96 384 192C384 279.4 267 435 215.7 499.2C203.4 514.5 180.6 514.5 168.3 499.2H168.3zM192 256C227.3 256 256 227.3 256 192C256 156.7 227.3 128 192 128C156.7 128 128 156.7 128 192C128 227.3 156.7 256 192 256z"></path>
#                                             </svg>
#                                         </i>
#                                     </a>
#                                 </div>
#                                                     </div>
#                         <div class="ss-hotel-single-gallery" id="maingallery">
#                             <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-لوگو.jpg" class="ss-hotel-single-gallery-main">
#                                 <span class="text-off">text off</span>
#                                 <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-لوگو.jpg"  class="image-1 lazyload" alt="عکس هتل بزرگ شیراز" />
#                             </a>
#                                                             <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-نمای-خارجی-2.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-نمای-خارجی-2.jpg" alt="عکس هتل بزرگ شیراز شماره 1">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-نمای-خارجی.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-نمای-خارجی.jpg" alt="عکس هتل بزرگ شیراز شماره 2">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سرویس-بهداشتی.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سرویس-بهداشتی.jpg" alt="عکس هتل بزرگ شیراز شماره 3">
#                                 </a>
#                                                             <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-لابی-پذیرش.jpg" class="ss-hotel-single-gallery-side-item">
#                                 <div class="ss-hotel-single-gallery-si-hover">
#                                     <span class="ss-hotel-single-gallery-sih-val">46+</span>
#                                     <span class="ss-hotel-single-gallery-sih-name">نمایش  تصاویر دیگر</span>
#                                 </div>
#                                 <span class="text-off">text off</span>
#                                 <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-لابی-پذیرش.jpg" alt="عکس هتل بزرگ شیراز" ">
#                             </a>
#
#                                                             <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-نمای-خارجی-3.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-نمای-خارجی-3.jpg" alt="عکس هتل بزرگ شیراز شماره 5">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-رستوران-7.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-رستوران-7.jpg" alt="عکس هتل بزرگ شیراز شماره 7">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-کافی-شاپ-1.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-کافی-شاپ-1.jpg" alt="عکس هتل بزرگ شیراز شماره 9">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-استخر-5.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-استخر-5.jpg" alt="عکس هتل بزرگ شیراز شماره 11">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-استخر-6.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-استخر-6.jpg" alt="عکس هتل بزرگ شیراز شماره 13">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-استخر-2.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-استخر-2.jpg" alt="عکس هتل بزرگ شیراز شماره 15">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سالن-6.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سالن-6.jpg" alt="عکس هتل بزرگ شیراز شماره 17">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سالن-7.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سالن-7.jpg" alt="عکس هتل بزرگ شیراز شماره 19">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-رستوران-4.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-رستوران-4.jpg" alt="عکس هتل بزرگ شیراز شماره 21">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-کافی-شاپ.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-کافی-شاپ.jpg" alt="عکس هتل بزرگ شیراز شماره 23">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سوئیت-6.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سوئیت-6.jpg" alt="عکس هتل بزرگ شیراز شماره 25">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سالن-4.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سالن-4.jpg" alt="عکس هتل بزرگ شیراز شماره 27">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سوئیت-3.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سوئیت-3.jpg" alt="عکس هتل بزرگ شیراز شماره 29">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سوئیت-7.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سوئیت-7.jpg" alt="عکس هتل بزرگ شیراز شماره 31">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-پارکینگ.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-پارکینگ.jpg" alt="عکس هتل بزرگ شیراز شماره 33">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-رختکن.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-رختکن.jpg" alt="عکس هتل بزرگ شیراز شماره 35">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-مرکز-خرید-1.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-مرکز-خرید-1.jpg" alt="عکس هتل بزرگ شیراز شماره 37">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-رستوران-8.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-رستوران-8.jpg" alt="عکس هتل بزرگ شیراز شماره 39">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-استخر.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-استخر.jpg" alt="عکس هتل بزرگ شیراز شماره 41">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سوئیت.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سوئیت.jpg" alt="عکس هتل بزرگ شیراز شماره 43">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سالن-5.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سالن-5.jpg" alt="عکس هتل بزرگ شیراز شماره 45">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-لابی-پذیرش-1.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-لابی-پذیرش-1.jpg" alt="عکس هتل بزرگ شیراز شماره 47">
#                                 </a>
#                                                                 <a href="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سالن-1.jpg" class="ss-hotel-single-gallery-side-item">
#                                     <span class="text-off">text off</span>
#                                     <img src="https://hotelyar.com/pic/726/عکس-هتل-بزرگ-شیراز-سالن-1.jpg" alt="عکس هتل بزرگ شیراز شماره 49">
#                                 </a>
#                                                         </div>
#                     </div>
#                 </div>
#             </div>
#         </section>
#         <!-- Ends: gallery -->
#         <!-- Start: Hotel Description 1&2 -->
#
#                 <!-- Ends: Hotel Description 1&2 -->
#         <!-- Start: Hotel Package -->
#                 <!-- Ends: Hotel Package -->
#         <!-- Start: features -->
#         <!--        -->        <!-- Ends: features -->
#         <!-- Start: reserve -->
#         <section>
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12">
#                         <div class="mb-search-wrapper">
#                                                             <div class="mb-search-title">
#                                     <div class="ss-innerpage-head-title small-text blue-text">
#                                         <i>
#                                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M488 400h-464C10.75 400 0 410.7 0 423.1C0 437.3 10.75 448 23.1 448h464c13.25 0 24-10.75 24-23.1C512 410.7 501.3 400 488 400zM80 352c0-97 79-176 176-176s176 79 176 176v16H480V352c0-112.9-83.5-205.9-192-221.5V112h24c13.25 0 24-10.75 24-24C336 74.74 325.3 64 311.1 64h-112C186.7 64 176 74.74 176 88c0 13.25 10.75 24 24 24H224v18.5C115.5 146.1 32 239.1 32 352v16h48V352z"/></svg>
#                                         </i>
#                                         <h2>رزرو هتل بزرگ شیراز </h2><span>100% آنلاین و 24 ساعته</span>                                    </div>
#                                 </div>
#                                                         <div class="mb-search-box box-shadow">
#                                                                     <div class="mb-search-title title-mobile">
#                                         <div class="ss-innerpage-head-title small-text blue-text">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M488 400h-464C10.75 400 0 410.7 0 423.1C0 437.3 10.75 448 23.1 448h464c13.25 0 24-10.75 24-23.1C512 410.7 501.3 400 488 400zM80 352c0-97 79-176 176-176s176 79 176 176v16H480V352c0-112.9-83.5-205.9-192-221.5V112h24c13.25 0 24-10.75 24-24C336 74.74 325.3 64 311.1 64h-112C186.7 64 176 74.74 176 88c0 13.25 10.75 24 24 24H224v18.5C115.5 146.1 32 239.1 32 352v16h48V352z"/></svg>
#                                             </i>
#                                             رزرو هتل بزرگ شیراز 100% آنلاین و 24 ساعته                                        </div>
#                                     </div>
#                                                                 <div class="mb-searchbox-v2-wrapper ">
#                                     <div class="ss-homt-sb-iw-cont date twoWay " >
#                                         <div class="ss-homt-sb-iw-cont-date-wrapper hotelsSearchSeg4">
#                                             <div class="searchbox-dropdown-cont" id="departureDate">
#                                                 <div type="text" class="form-control input mb-sb-input-v2 searchbox-date-input-di floating-input departureDate " required="">1403/11/14</div>
#                                                 <label class="floating-label departureDateDetails "><strong>تاریخ ورود </strong></label>
#                                                 <span class="label-error fromDate-label-error color-red "></span>
#                                             </div>
#                                             <div class="searchbox-dropdown-cont oneway"  id="returnDate">
#                                                 <div type="text" class="form-control input mb-sb-input-v2 searchbox-date-input-do floating-input returnDate" required="">1403/11/15</div>
#                                                 <label class="floating-label returnDateDetails"><strong>تاریخ خروج </strong></label>
#                                                 <span class="label-error toDate-label-error color-red"></span>
#                                             </div>
#                                         </div>
#                                     </div>
#                                                                             <div class="ss-homt-sb-iw-cont city">
#                                             <span class="ss-hotel-sginle-search-text-day color-gray">شروع قیمت رزرو به مدت<span> 1 شب</span></span>
#                                                                                             <strike class="ss-hotel-sginle-search-text-price color-gray">3,793,900</strike>
#                                                                                         <span class="ss-hotel-sginle-search-text-price ">3,376,000</span>
#                                         </div>
#                                                                         <div class="ss-homt-sb-iw-cont search">
#                                         <form  id="hotelFrmSearch" method="post" action="https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز#div-search">
#                                                                                         <input type="hidden" class="fromDate" name="fromDate" value="1403/11/14" >
#                                             <input type="hidden" class="fromDateDetails" name="fromDateDetails" value="یک‌شنبه - 14 بهمن" >
#                                             <input type="hidden" class="toDate" name="toDate" value="1403/11/15" >
#                                             <input type="hidden" class="toDateDetails" name="toDateDetails" value="دوشنبه - 15 بهمن" >
#                                         </form>
#                                         <button type="button" class="btn ss-btn ss-btn-red ss-btn-large mb-sb-btn" id="hotelSearchBoxBtn" aria-label="Name">
#                                             <span>جستجوی مجدد</span>
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path>
#                                                 </svg>
#                                             </i>
#                                         </button>
#                                     </div>
#                                 </div>
#                             </div>
#                         </div>
#
#
#                         <h3 class="ss-innerpage-head-title small-text">
#                             <i>
#                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><path d="M168 304C216.5 304 256 264.5 256 216S216.5 128 168 128S80 167.5 80 216S119.5 304 168 304zM168 176c21.1 0 40 18 40 40C208 238 189.1 256 168 256C145.1 256 128 238 128 216C128 194 145.1 176 168 176zM528 128h-224C295.2 128 288 135.2 288 144v192H48v-280C48 42.75 37.25 32 24 32S0 42.75 0 55.1V456C0 469.3 10.75 480 23.1 480S48 469.3 48 456V384h544v72C592 469.3 602.7 480 616 480S640 469.3 640 456V240C640 178.1 589.9 128 528 128zM592 336h-256v-160h192c35.25 0 64 28.75 64 64V336z"/></svg>
#                             </i>لیست قیمت اتاق ها<span class="color-gray iranyekan">(قیمت ها به تومان می باشد)</span>
#                         </h3>
#                                                         <form id="frmReservation" method="post" action="https://hotelyar.com/uiReservationGroup.php">
#                                     <input type="hidden" name="hotelCode" value="726">
#                                     <input type="hidden" name="fromDate" value="1403/11/14">
#                                     <input type="hidden" name="toDate" value="1403/11/15">
#
#                                     <div class="ss-reserve-block-list" id="book">
#                                         <table class="ss-reserve-table responsive">
#                                             <thead>
#                                             <tr>
#                                                 <th>نوع اتاق</th>
#                                                                                                     <th>ظرفیت</th>
#                                                     <th>صبحانه</th>
#                                                     <th>تخفیف</th>
#                                                                                                 <th>سرویس اضافه</th>
#                                                 <th>یک‌شنبه<br>14 بهمن</th>                                                <th>جمع پرداختی<br>1 شب</th>
#                                                 <th>تعداد اتاق</th>
#                                             </tr>
#                                             </thead>
#                                             <tbody>
#                                                 <tr>
#         <td  data-title="نوع اتاق"  >
#             <div class="ss-reserve-table-content-wrapper">
#                                 <div class="ss-reserve-table-content">
#                     <span class="ss-reserve-table-c-title">اتاق دو تخته برای یکنفر</span>
#                     <span class="ss-reserve-table-c-sub color-gray">
#                                                 </span>
#                                                                         <div class="ss-reserve-table-c-reward">
#                                 <i>
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 101L294.8 38.97C309.9 14.73 336.5 0 365.1 0H368C412.2 0 448 35.82 448 80C448 98.01 442 114.6 432 128H464C490.5 128 512 149.5 512 176V240C512 260.9 498.6 278.7 480 285.3V448C480 483.3 451.3 512 416 512H96C60.65 512 32 483.3 32 448V285.3C13.36 278.7 0 260.9 0 240V176C0 149.5 21.49 128 48 128H79.99C69.95 114.6 64 98.01 64 80C64 35.82 99.82 0 144 0H146.9C175.5 0 202.1 14.73 217.2 38.97L256 101zM365.1 32C347.5 32 331.2 41.04 321.9 55.93L276.9 128H368C394.5 128 416 106.5 416 80C416 53.49 394.5 32 368 32H365.1zM235.1 128L190.1 55.93C180.8 41.04 164.5 32 146.9 32H144C117.5 32 96 53.49 96 80C96 106.5 117.5 128 144 128H235.1zM48 160C39.16 160 32 167.2 32 176V240C32 248.8 39.16 256 48 256H240V160H48zM272 256H464C472.8 256 480 248.8 480 240V176C480 167.2 472.8 160 464 160H272V256zM240 288H64V448C64 465.7 78.33 480 96 480H240V288zM272 480H416C433.7 480 448 465.7 448 448V288H272V480z"></path>
#                                     </svg>
#                                 </i>
#                                 <span>تا 68 امتیاز</span>
#                             </div>
#                                                             </div>
#             </div>
#                     </td>
#                     <td data-title="ظرفیت (نفر)">
#                 <div class="ss-reserve-table-cap">
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><path d="M160 160H96C60.65 160 32 188.7 32 224v96c0 17.67 14.33 32 32 32v144C64 504.8 71.16 512 80 512S96 504.8 96 496V352h64v144c0 8.844 7.156 16 16 16s16-7.156 16-16V352c17.67 0 32-14.33 32-32V224C224 188.7 195.3 160 160 160zM192 320H64V224c0-17.64 14.36-32 32-32h64c17.64 0 32 14.36 32 32V320zM128 128c35.38 0 64-28.62 64-64s-28.62-64-64-64S64 28.62 64 64S92.63 128 128 128zM128 32c17.64 0 32 14.36 32 32s-14.36 32-32 32S96 81.64 96 64S110.4 32 128 32z"/></svg>
#                         </i>
#                                     </div>
#             </td>
#             <td data-title="صبحانه">
#                 <div class="ss-reserve-table-option">
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M440.1 103C450.3 112.4 450.3 127.6 440.1 136.1L176.1 400.1C167.6 410.3 152.4 410.3 143 400.1L7.029 264.1C-2.343 255.6-2.343 240.4 7.029 231C16.4 221.7 31.6 221.7 40.97 231L160 350.1L407 103C416.4 93.66 431.6 93.66 440.1 103V103z"/>
#                             </svg>
#                         </i>
#                                     </div>
#             </td>
#             <td data-title="تخفیف ویژه رزرو">
#                 <div class="color-red ss-reserve-table-off">
#                     %11                </div>
#             </td>
#             <td data-title="سرویس اضافه (نفر)">
#                 <div class="ss-reserve-table-service">
#                     -                </div>
#             </td>
#                             <td data-title="یک‌شنبه چهاردهم بهمن" class="ss-red ss-no">
#                                                     <span class="ss-reserve-table-p-off color-gray">3,793,900</span>
#                                                     <span class="ss-reserve-table-p-val ">
#                         3,376,000                        </span>
#                         جا ندارد
#                     </td>
#                                 <td class="ss-red ss-no" data-title="جمع پرداختی1شب">
#                                     <span class="ss-reserve-table-p-off color-gray">3,793,900</span>
#                                     <span class="ss-reserve-table-p-fullval ">
#                 3,376,000                </span>
#                 جا ندارد
#             </td>
#
#                 <td data-title="">
#                     <button type="button" class="btn ss-btn ss-btn-red ss-reserve-table-btn item" onclick="waitBook(this,1)">لیست انتظار</button>
#                 </td>
#                 </tr>
#         <tr>
#         <td  data-title="نوع اتاق"  >
#             <div class="ss-reserve-table-content-wrapper">
#                                 <div class="ss-reserve-table-content">
#                     <span class="ss-reserve-table-c-title">اتاق دو تخته</span>
#                     <span class="ss-reserve-table-c-sub color-gray">
#                             دبل                    </span>
#                                                                         <div class="ss-reserve-table-c-reward">
#                                 <i>
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 101L294.8 38.97C309.9 14.73 336.5 0 365.1 0H368C412.2 0 448 35.82 448 80C448 98.01 442 114.6 432 128H464C490.5 128 512 149.5 512 176V240C512 260.9 498.6 278.7 480 285.3V448C480 483.3 451.3 512 416 512H96C60.65 512 32 483.3 32 448V285.3C13.36 278.7 0 260.9 0 240V176C0 149.5 21.49 128 48 128H79.99C69.95 114.6 64 98.01 64 80C64 35.82 99.82 0 144 0H146.9C175.5 0 202.1 14.73 217.2 38.97L256 101zM365.1 32C347.5 32 331.2 41.04 321.9 55.93L276.9 128H368C394.5 128 416 106.5 416 80C416 53.49 394.5 32 368 32H365.1zM235.1 128L190.1 55.93C180.8 41.04 164.5 32 146.9 32H144C117.5 32 96 53.49 96 80C96 106.5 117.5 128 144 128H235.1zM48 160C39.16 160 32 167.2 32 176V240C32 248.8 39.16 256 48 256H240V160H48zM272 256H464C472.8 256 480 248.8 480 240V176C480 167.2 472.8 160 464 160H272V256zM240 288H64V448C64 465.7 78.33 480 96 480H240V288zM272 480H416C433.7 480 448 465.7 448 448V288H272V480z"></path>
#                                     </svg>
#                                 </i>
#                                 <span>تا 118 امتیاز</span>
#                             </div>
#                                                             </div>
#             </div>
#                     </td>
#                     <td data-title="ظرفیت (نفر)">
#                 <div class="ss-reserve-table-cap">
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><path d="M160 160H96C60.65 160 32 188.7 32 224v96c0 17.67 14.33 32 32 32v144C64 504.8 71.16 512 80 512S96 504.8 96 496V352h64v144c0 8.844 7.156 16 16 16s16-7.156 16-16V352c17.67 0 32-14.33 32-32V224C224 188.7 195.3 160 160 160zM192 320H64V224c0-17.64 14.36-32 32-32h64c17.64 0 32 14.36 32 32V320zM128 128c35.38 0 64-28.62 64-64s-28.62-64-64-64S64 28.62 64 64S92.63 128 128 128zM128 32c17.64 0 32 14.36 32 32s-14.36 32-32 32S96 81.64 96 64S110.4 32 128 32z"/></svg>
#                         </i>
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><path d="M160 160H96C60.65 160 32 188.7 32 224v96c0 17.67 14.33 32 32 32v144C64 504.8 71.16 512 80 512S96 504.8 96 496V352h64v144c0 8.844 7.156 16 16 16s16-7.156 16-16V352c17.67 0 32-14.33 32-32V224C224 188.7 195.3 160 160 160zM192 320H64V224c0-17.64 14.36-32 32-32h64c17.64 0 32 14.36 32 32V320zM128 128c35.38 0 64-28.62 64-64s-28.62-64-64-64S64 28.62 64 64S92.63 128 128 128zM128 32c17.64 0 32 14.36 32 32s-14.36 32-32 32S96 81.64 96 64S110.4 32 128 32z"/></svg>
#                         </i>
#                                     </div>
#             </td>
#             <td data-title="صبحانه">
#                 <div class="ss-reserve-table-option">
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M440.1 103C450.3 112.4 450.3 127.6 440.1 136.1L176.1 400.1C167.6 410.3 152.4 410.3 143 400.1L7.029 264.1C-2.343 255.6-2.343 240.4 7.029 231C16.4 221.7 31.6 221.7 40.97 231L160 350.1L407 103C416.4 93.66 431.6 93.66 440.1 103V103z"/>
#                             </svg>
#                         </i>
#                                     </div>
#             </td>
#             <td data-title="تخفیف ویژه رزرو">
#                 <div class="color-red ss-reserve-table-off">
#                     %21                </div>
#             </td>
#             <td data-title="سرویس اضافه (نفر)">
#                 <div class="ss-reserve-table-service">
#                     1                </div>
#             </td>
#                             <td data-title="یک‌شنبه چهاردهم بهمن" class="ss-red ss-no">
#                                                     <span class="ss-reserve-table-p-off color-gray">6,587,900</span>
#                                                     <span class="ss-reserve-table-p-val ">
#                         5,204,000                        </span>
#                         جا ندارد
#                     </td>
#                                 <td class="ss-red ss-no" data-title="جمع پرداختی1شب">
#                                     <span class="ss-reserve-table-p-off color-gray">6,587,900</span>
#                                     <span class="ss-reserve-table-p-fullval ">
#                 5,204,000                </span>
#                 جا ندارد
#             </td>
#
#                 <td data-title="">
#                     <button type="button" class="btn ss-btn ss-btn-red ss-reserve-table-btn item" onclick="waitBook(this,2)">لیست انتظار</button>
#                 </td>
#                 </tr>
#         <tr>
#         <td  data-title="نوع اتاق"  >
#             <div class="ss-reserve-table-content-wrapper">
#                                 <div class="ss-reserve-table-content">
#                     <span class="ss-reserve-table-c-title">اتاق دو تخته</span>
#                     <span class="ss-reserve-table-c-sub color-gray">
#                             تویین                    </span>
#                                                                         <div class="ss-reserve-table-c-reward">
#                                 <i>
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 101L294.8 38.97C309.9 14.73 336.5 0 365.1 0H368C412.2 0 448 35.82 448 80C448 98.01 442 114.6 432 128H464C490.5 128 512 149.5 512 176V240C512 260.9 498.6 278.7 480 285.3V448C480 483.3 451.3 512 416 512H96C60.65 512 32 483.3 32 448V285.3C13.36 278.7 0 260.9 0 240V176C0 149.5 21.49 128 48 128H79.99C69.95 114.6 64 98.01 64 80C64 35.82 99.82 0 144 0H146.9C175.5 0 202.1 14.73 217.2 38.97L256 101zM365.1 32C347.5 32 331.2 41.04 321.9 55.93L276.9 128H368C394.5 128 416 106.5 416 80C416 53.49 394.5 32 368 32H365.1zM235.1 128L190.1 55.93C180.8 41.04 164.5 32 146.9 32H144C117.5 32 96 53.49 96 80C96 106.5 117.5 128 144 128H235.1zM48 160C39.16 160 32 167.2 32 176V240C32 248.8 39.16 256 48 256H240V160H48zM272 256H464C472.8 256 480 248.8 480 240V176C480 167.2 472.8 160 464 160H272V256zM240 288H64V448C64 465.7 78.33 480 96 480H240V288zM272 480H416C433.7 480 448 465.7 448 448V288H272V480z"></path>
#                                     </svg>
#                                 </i>
#                                 <span>تا 118 امتیاز</span>
#                             </div>
#                                                             </div>
#             </div>
#                     </td>
#                     <td data-title="ظرفیت (نفر)">
#                 <div class="ss-reserve-table-cap">
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><path d="M160 160H96C60.65 160 32 188.7 32 224v96c0 17.67 14.33 32 32 32v144C64 504.8 71.16 512 80 512S96 504.8 96 496V352h64v144c0 8.844 7.156 16 16 16s16-7.156 16-16V352c17.67 0 32-14.33 32-32V224C224 188.7 195.3 160 160 160zM192 320H64V224c0-17.64 14.36-32 32-32h64c17.64 0 32 14.36 32 32V320zM128 128c35.38 0 64-28.62 64-64s-28.62-64-64-64S64 28.62 64 64S92.63 128 128 128zM128 32c17.64 0 32 14.36 32 32s-14.36 32-32 32S96 81.64 96 64S110.4 32 128 32z"/></svg>
#                         </i>
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><path d="M160 160H96C60.65 160 32 188.7 32 224v96c0 17.67 14.33 32 32 32v144C64 504.8 71.16 512 80 512S96 504.8 96 496V352h64v144c0 8.844 7.156 16 16 16s16-7.156 16-16V352c17.67 0 32-14.33 32-32V224C224 188.7 195.3 160 160 160zM192 320H64V224c0-17.64 14.36-32 32-32h64c17.64 0 32 14.36 32 32V320zM128 128c35.38 0 64-28.62 64-64s-28.62-64-64-64S64 28.62 64 64S92.63 128 128 128zM128 32c17.64 0 32 14.36 32 32s-14.36 32-32 32S96 81.64 96 64S110.4 32 128 32z"/></svg>
#                         </i>
#                                     </div>
#             </td>
#             <td data-title="صبحانه">
#                 <div class="ss-reserve-table-option">
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M440.1 103C450.3 112.4 450.3 127.6 440.1 136.1L176.1 400.1C167.6 410.3 152.4 410.3 143 400.1L7.029 264.1C-2.343 255.6-2.343 240.4 7.029 231C16.4 221.7 31.6 221.7 40.97 231L160 350.1L407 103C416.4 93.66 431.6 93.66 440.1 103V103z"/>
#                             </svg>
#                         </i>
#                                     </div>
#             </td>
#             <td data-title="تخفیف ویژه رزرو">
#                 <div class="color-red ss-reserve-table-off">
#                     %21                </div>
#             </td>
#             <td data-title="سرویس اضافه (نفر)">
#                 <div class="ss-reserve-table-service">
#                     1                </div>
#             </td>
#                             <td data-title="یک‌شنبه چهاردهم بهمن" class="ss-red ss-no">
#                                                     <span class="ss-reserve-table-p-off color-gray">6,587,900</span>
#                                                     <span class="ss-reserve-table-p-val ">
#                         5,204,000                        </span>
#                         جا ندارد
#                     </td>
#                                 <td class="ss-red ss-no" data-title="جمع پرداختی1شب">
#                                     <span class="ss-reserve-table-p-off color-gray">6,587,900</span>
#                                     <span class="ss-reserve-table-p-fullval ">
#                 5,204,000                </span>
#                 جا ندارد
#             </td>
#
#                 <td data-title="">
#                     <button type="button" class="btn ss-btn ss-btn-red ss-reserve-table-btn item" onclick="waitBook(this,6)">لیست انتظار</button>
#                 </td>
#                 </tr>
#         <tr>
#         <td  data-title="نوع اتاق"  >
#             <div class="ss-reserve-table-content-wrapper">
#                                 <div class="ss-reserve-table-content">
#                     <span class="ss-reserve-table-c-title">سوئیت کانکت</span>
#                     <span class="ss-reserve-table-c-sub color-gray">
#                                                 </span>
#                                                                         <div class="ss-reserve-table-c-reward">
#                                 <i>
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 101L294.8 38.97C309.9 14.73 336.5 0 365.1 0H368C412.2 0 448 35.82 448 80C448 98.01 442 114.6 432 128H464C490.5 128 512 149.5 512 176V240C512 260.9 498.6 278.7 480 285.3V448C480 483.3 451.3 512 416 512H96C60.65 512 32 483.3 32 448V285.3C13.36 278.7 0 260.9 0 240V176C0 149.5 21.49 128 48 128H79.99C69.95 114.6 64 98.01 64 80C64 35.82 99.82 0 144 0H146.9C175.5 0 202.1 14.73 217.2 38.97L256 101zM365.1 32C347.5 32 331.2 41.04 321.9 55.93L276.9 128H368C394.5 128 416 106.5 416 80C416 53.49 394.5 32 368 32H365.1zM235.1 128L190.1 55.93C180.8 41.04 164.5 32 146.9 32H144C117.5 32 96 53.49 96 80C96 106.5 117.5 128 144 128H235.1zM48 160C39.16 160 32 167.2 32 176V240C32 248.8 39.16 256 48 256H240V160H48zM272 256H464C472.8 256 480 248.8 480 240V176C480 167.2 472.8 160 464 160H272V256zM240 288H64V448C64 465.7 78.33 480 96 480H240V288zM272 480H416C433.7 480 448 465.7 448 448V288H272V480z"></path>
#                                     </svg>
#                                 </i>
#                                 <span>تا 161 امتیاز</span>
#                             </div>
#                                                             </div>
#             </div>
#                     </td>
#                     <td data-title="ظرفیت (نفر)">
#                 <div class="ss-reserve-table-cap">
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><path d="M160 160H96C60.65 160 32 188.7 32 224v96c0 17.67 14.33 32 32 32v144C64 504.8 71.16 512 80 512S96 504.8 96 496V352h64v144c0 8.844 7.156 16 16 16s16-7.156 16-16V352c17.67 0 32-14.33 32-32V224C224 188.7 195.3 160 160 160zM192 320H64V224c0-17.64 14.36-32 32-32h64c17.64 0 32 14.36 32 32V320zM128 128c35.38 0 64-28.62 64-64s-28.62-64-64-64S64 28.62 64 64S92.63 128 128 128zM128 32c17.64 0 32 14.36 32 32s-14.36 32-32 32S96 81.64 96 64S110.4 32 128 32z"/></svg>
#                         </i>
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><path d="M160 160H96C60.65 160 32 188.7 32 224v96c0 17.67 14.33 32 32 32v144C64 504.8 71.16 512 80 512S96 504.8 96 496V352h64v144c0 8.844 7.156 16 16 16s16-7.156 16-16V352c17.67 0 32-14.33 32-32V224C224 188.7 195.3 160 160 160zM192 320H64V224c0-17.64 14.36-32 32-32h64c17.64 0 32 14.36 32 32V320zM128 128c35.38 0 64-28.62 64-64s-28.62-64-64-64S64 28.62 64 64S92.63 128 128 128zM128 32c17.64 0 32 14.36 32 32s-14.36 32-32 32S96 81.64 96 64S110.4 32 128 32z"/></svg>
#                         </i>
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><path d="M160 160H96C60.65 160 32 188.7 32 224v96c0 17.67 14.33 32 32 32v144C64 504.8 71.16 512 80 512S96 504.8 96 496V352h64v144c0 8.844 7.156 16 16 16s16-7.156 16-16V352c17.67 0 32-14.33 32-32V224C224 188.7 195.3 160 160 160zM192 320H64V224c0-17.64 14.36-32 32-32h64c17.64 0 32 14.36 32 32V320zM128 128c35.38 0 64-28.62 64-64s-28.62-64-64-64S64 28.62 64 64S92.63 128 128 128zM128 32c17.64 0 32 14.36 32 32s-14.36 32-32 32S96 81.64 96 64S110.4 32 128 32z"/></svg>
#                         </i>
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><path d="M160 160H96C60.65 160 32 188.7 32 224v96c0 17.67 14.33 32 32 32v144C64 504.8 71.16 512 80 512S96 504.8 96 496V352h64v144c0 8.844 7.156 16 16 16s16-7.156 16-16V352c17.67 0 32-14.33 32-32V224C224 188.7 195.3 160 160 160zM192 320H64V224c0-17.64 14.36-32 32-32h64c17.64 0 32 14.36 32 32V320zM128 128c35.38 0 64-28.62 64-64s-28.62-64-64-64S64 28.62 64 64S92.63 128 128 128zM128 32c17.64 0 32 14.36 32 32s-14.36 32-32 32S96 81.64 96 64S110.4 32 128 32z"/></svg>
#                         </i>
#                                     </div>
#             </td>
#             <td data-title="صبحانه">
#                 <div class="ss-reserve-table-option">
#                                             <i>
#                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M440.1 103C450.3 112.4 450.3 127.6 440.1 136.1L176.1 400.1C167.6 410.3 152.4 410.3 143 400.1L7.029 264.1C-2.343 255.6-2.343 240.4 7.029 231C16.4 221.7 31.6 221.7 40.97 231L160 350.1L407 103C416.4 93.66 431.6 93.66 440.1 103V103z"/>
#                             </svg>
#                         </i>
#                                     </div>
#             </td>
#             <td data-title="تخفیف ویژه رزرو">
#                 <div class="color-red ss-reserve-table-off">
#                     %11                </div>
#             </td>
#             <td data-title="سرویس اضافه (نفر)">
#                 <div class="ss-reserve-table-service">
#                     -                </div>
#             </td>
#                             <td data-title="یک‌شنبه چهاردهم بهمن" class="ss-red ss-no">
#                                                     <span class="ss-reserve-table-p-off color-gray">8,962,800</span>
#                                                     <span class="ss-reserve-table-p-val ">
#                         7,976,000                        </span>
#                         جا ندارد
#                     </td>
#                                 <td class="ss-red ss-no" data-title="جمع پرداختی1شب">
#                                     <span class="ss-reserve-table-p-off color-gray">8,962,800</span>
#                                     <span class="ss-reserve-table-p-fullval ">
#                 7,976,000                </span>
#                 جا ندارد
#             </td>
#
#                 <td data-title="">
#                     <button type="button" class="btn ss-btn ss-btn-red ss-reserve-table-btn item" onclick="waitBook(this,9)">لیست انتظار</button>
#                 </td>
#                 </tr>
#                                                 </tbody>
#
#                                             <tfoot>
#                                             <tr>
#                                                 <td class="extraText" colspan="8">
#                                                     <span class='text-center '>قیمت نفر اضافه برای یک شب به ازای هر نفر &nbsp;<strike>1,736,900</strike>&nbsp; 1,545,000 تومان می باشد</span>                                                </td>
#                                             </tr>
#                                             </tfoot>
#                                         </table>
#                                                                                     <style>
#                                                 .ss-reserve-table {
#                                                     width: 100% !important;
#                                                     border-collapse: separate;
#                                                     border-spacing: 0 10px;
#                                                 }
#                                             </style>
#                                                                             </div>
#                                 </form>
#                                                     </div>
#                 </div>
#             </div>
#         </section>
#         <!-- Ends: reserve -->
#         <!-- Start: panaroma -->
#         <section class="ss-hotel-single-panorama-section">
#                     </section>
#         <!-- Ends: panaroma -->
#         <!-- Start: Hotel Description 3&4 -->
#
#                     <section>
#                 <div class="ss-inner-main-bg"></div>
#                 <div class="container">
#                     <div class="row">
#                         <div class="col-md-12">
#                             <div class="ss-hotel-single-head-package">
#                                 <div class="ss-hotel-single-head-content-package">
#                                     <div class="ss-hotel-single-h-header-wrapper-package">
#                                                                                     <div class="ss-hotel-single-hhw-title-package">
#                                                 <h3 class="ss-hotel-single-hhwt-package-name">تسهیلات ویژه هتل بزرگ شیراز</h3>
#                                             </div>
#                                             <div class="ss-hotel-single-dr-list-single" id="single-scroll">
#                                                 <p>
#                                                     هتل بزرگ شیراز دارای  ترانسفر فرودگاهی رفت و برگشت با پرداخت هزینه میباشد.<br>خدمات رایگان هتل بزرگ شیراز شامل صبحانه و مجموعه ورزشی ( استخر، سونا، جکوزی، باشگاه بدنسازی و صخره نوردی) می باشد. لازم به ذکر است ساعات استفاده رایگان از مجموعه آبی و سالن بدن سازی در ساعات 8:00 الی 14:00 و 15:00 الی 18:00 می باشد.                                                </p>
#                                             </div>
#
#                                                                                     <div class="ss-title">
#                                                 <h3 class="ss-hotel-single-hhwt-package-name mt-3">توضیحات مهم هتل بزرگ شیراز</h3>
#                                             </div>
#                                             <div class="ss-single-abt-c-notice">
#                                                 <p class="more-text">
#                                                     هزینه اقامت برای کودکان زیر 3 سال در صورت عدم استفاده از سرویس اضافه رایگان و برای سنین بین 3 تا 7 سال در صورت عدم استفاده از سرویس نیم بها محاسبه می گردد.<br />
# سرویس اضافه به صورت تخت ارائه می گردد.<br />
# پذیرش صیغه نامه معتبر با مهر برجسته امکان پذیر می باشد.<br />
# استفاده از استخر هتل، برای کودکان زیر 9 سال امکان پذیر نمی باشد.<br />
# قوانین کنسلی :<br />
# قوانین کنسلی بسته به شرایط و زمان لغو رزرو، متفاوت است.                                                </p>
#                                             </div>
#                                                                             </div>
#                                 </div>
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#             </section>
#                 <!-- Ends: Hotel Description 3&4 -->
#         <!-- Start: rating -->
#                     <section class="ss-hotel-single-rating-section">
#                 <div class="ss-inner-main-bg rotate bottom"></div>
#                 <div class="container">
#                     <div class="row">
#                         <div class="col-md-12">
#                             <h3 class="ss-innerpage-head-title">
#                                 <i>
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M240 32C266.5 32 288 53.49 288 80V432C288 458.5 266.5 480 240 480H208C181.5 480 160 458.5 160 432V80C160 53.49 181.5 32 208 32H240zM240 80H208V432H240V80zM80 224C106.5 224 128 245.5 128 272V432C128 458.5 106.5 480 80 480H48C21.49 480 0 458.5 0 432V272C0 245.5 21.49 224 48 224H80zM80 272H48V432H80V272zM320 144C320 117.5 341.5 96 368 96H400C426.5 96 448 117.5 448 144V432C448 458.5 426.5 480 400 480H368C341.5 480 320 458.5 320 432V144zM368 432H400V144H368V432z"/></svg>
#                                 </i>امتیاز مسافران به  هتل بزرگ شیراز                            </h3>
#                             <div class="ss-hotel-single-rating-box">
#                                                                     <div class="ss-hotel-single-rb-header">
#                                         <div class="ss-hotel-single-rbh-brate ">4.7</div>
#                                         <div class="ss-hotel-single-rbh-text">امتیاز <span class="ss-hotel-single-rbht-point color-blue">
#                                                                         <span>4.7                                        <span class="color-gray ss-hotel-single-rbht-small">توسط <span>27</span> مسافر</span>
#                                         </div>
#                                     </div>
#                                                                 <div class="ss-hotel-single-rb-pc-wrapper">
#                                                                             <div class="ss-hotel-single-rb-poll">
#                                             <div class="tab-content ss-hotel-single-rbp-content" id="nav-tabContent">
#                                                                                                 <div class="tab-pane fade show active" id="nav-1" role="tabpanel" aria-labelledby="nav-1-tab">
#                                                         <div class="ss-hotel-single-rb-poll-list">
#                     <div class="skillbar-item">
#                 <div class="skillbar-title color-gray">
#                     <span>برخورد کارکنان</span>
#                 </div>
#                 <div class="skill-bar-percent">100%</div>
#                 <div class="skillbar clearfix" data-percent="100%">
#                     <div class="skillbar-bar"
#                          style="width: 100%; background: #12c445;"></div>
#                 </div>
#             </div>
#                         <div class="skillbar-item">
#                 <div class="skillbar-title color-gray">
#                     <span>تمیزی اتاق ها و لابی هتل</span>
#                 </div>
#                 <div class="skill-bar-percent">100%</div>
#                 <div class="skillbar clearfix" data-percent="100%">
#                     <div class="skillbar-bar"
#                          style="width: 100%; background: #12c445;"></div>
#                 </div>
#             </div>
#                         <div class="skillbar-item">
#                 <div class="skillbar-title color-gray">
#                     <span>کیفیت رستوران و کافی شاپ</span>
#                 </div>
#                 <div class="skill-bar-percent">100%</div>
#                 <div class="skillbar clearfix" data-percent="100%">
#                     <div class="skillbar-bar"
#                          style="width: 100%; background: #12c445;"></div>
#                 </div>
#             </div>
#                         <div class="skillbar-item">
#                 <div class="skillbar-title color-gray">
#                     <span>موقعیت مکانی هتل</span>
#                 </div>
#                 <div class="skill-bar-percent">100%</div>
#                 <div class="skillbar clearfix" data-percent="100%">
#                     <div class="skillbar-bar"
#                          style="width: 100%; background: #12c445;"></div>
#                 </div>
#             </div>
#                         <div class="skillbar-item">
#                 <div class="skillbar-title color-gray">
#                     <span>رضایت از قیمت نسبت به کیفیت</span>
#                 </div>
#                 <div class="skill-bar-percent">9%</div>
#                 <div class="skillbar clearfix" data-percent="9%">
#                     <div class="skillbar-bar"
#                          style="width: 9%; background: #d32f2f;"></div>
#                 </div>
#             </div>
#                         <div class="skillbar-item">
#                 <div class="skillbar-title color-gray">
#                     <span>توصیه به دیگران</span>
#                 </div>
#                 <div class="skill-bar-percent">100%</div>
#                 <div class="skillbar clearfix" data-percent="100%">
#                     <div class="skillbar-bar"
#                          style="width: 100%; background: #12c445;"></div>
#                 </div>
#             </div>
#                 </div>
#                                                     </div>
#
#                                             </div>
#                                         </div>
#                                                                                                                 <div class="ss-hotel-single-rb-comment">
#                                             <h4 class="ss-innerpage-head-title more-link">
#                                                 <div class="ss-innerpage-head-title-right">
#                                                     <i>
#                                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M360 144h-208C138.8 144 128 154.8 128 168S138.8 192 152 192h208C373.3 192 384 181.3 384 168S373.3 144 360 144zM264 240h-112C138.8 240 128 250.8 128 264S138.8 288 152 288h112C277.3 288 288 277.3 288 264S277.3 240 264 240zM447.1 0h-384c-35.25 0-64 28.75-64 63.1v287.1c0 35.25 28.75 63.1 64 63.1h96v83.1c0 9.836 11.02 15.55 19.12 9.7l124.9-93.7h144c35.25 0 64-28.75 64-63.1V63.1C511.1 28.75 483.2 0 447.1 0zM464 352c0 8.75-7.25 16-16 16h-160l-80 60v-60H64c-8.75 0-16-7.25-16-16V64c0-8.75 7.25-16 16-16h384c8.75 0 16 7.25 16 16V352z"/></svg>
#                                                     </i>نظر مسافران
#                                                 </div>
#                                                 <a href="#section-comments" class="ss-innerpage-head-title-left">
#                                                     <span class="iranyekan">مشاهده کامل</span>
#                                                     <i>
#                                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 512"><path d="M203.9 405.3c5.877 6.594 5.361 16.69-1.188 22.62c-6.562 5.906-16.69 5.375-22.59-1.188L36.1 266.7c-5.469-6.125-5.469-15.31 0-21.44l144-159.1c5.906-6.562 16.03-7.094 22.59-1.188c6.918 6.271 6.783 16.39 1.188 22.62L69.53 256L203.9 405.3z"></path></svg>
#                                                     </i>
#                                                 </a>
#                                             </h4>
#                                             <div class="ss-hotel-single-rbc-cmslider owl-carousel owl-theme">
#                                                                                                     <div class="ss-hotel-single-rbccm-item">
#                                                         <div class="ss-hotel-single-rbccm-i-box">
#                                                             <p>بسیادر تمیز</p>
#                                                         </div>
#                                                         <div class="ss-hotel-single-rbccm-i-footer">
#                                                             <span class="ss-hotel-single-rbccm-if-rate  color-blue"> 4 از 5 </span>
#                                                             <div class="ss-hotel-single-rbccm-if-content">
#                                                                 <span class="ss-hotel-single-rbccm-ifc-name">حسنین ارکوازی</span>
#                                                                 <span class="ss-hotel-single-rbccm-ifc-meta color-gray">نوشته شده در هشتم آبان 1403</span>
#                                                             </div>
#                                                         </div>
#                                                     </div>
#                                                                                                         <div class="ss-hotel-single-rbccm-item">
#                                                         <div class="ss-hotel-single-rbccm-i-box">
#                                                             <p>بعضی از پرسنل پذیرش (احتمالا بابت شلوغی) در انتقال اطلاعات ضعیف بودن و گاهی حس مثبت نداشتیم از تعامل باهاشون.
# در کل افامت خوبی بود و خوش گذشت.</p>
#                                                         </div>
#                                                         <div class="ss-hotel-single-rbccm-i-footer">
#                                                             <span class="ss-hotel-single-rbccm-if-rate  color-blue"> 4 از 5 </span>
#                                                             <div class="ss-hotel-single-rbccm-if-content">
#                                                                 <span class="ss-hotel-single-rbccm-ifc-name">محمدعلی کریمی</span>
#                                                                 <span class="ss-hotel-single-rbccm-ifc-meta color-gray">نوشته شده در بیست و هشتم مهر 1403</span>
#                                                             </div>
#                                                         </div>
#                                                     </div>
#                                                                                                         <div class="ss-hotel-single-rbccm-item">
#                                                         <div class="ss-hotel-single-rbccm-i-box">
#                                                             <p>همه چیز بسیار خوب</p>
#                                                         </div>
#                                                         <div class="ss-hotel-single-rbccm-i-footer">
#                                                             <span class="ss-hotel-single-rbccm-if-rate  color-blue"> 4 از 5 </span>
#                                                             <div class="ss-hotel-single-rbccm-if-content">
#                                                                 <span class="ss-hotel-single-rbccm-ifc-name">علیرضا پیوند</span>
#                                                                 <span class="ss-hotel-single-rbccm-ifc-meta color-gray">نوشته شده در بیست و چهارم شهریور 1403</span>
#                                                             </div>
#                                                         </div>
#                                                     </div>
#                                                                                                 </div>
#                                         </div>
#                                                                     </div>
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#             </section>
#                 <!-- Ends: rating -->
#
#
#         <!--   fixme:this section need to data entry     -->
#                         <!--   fixme:this section need to data entry     -->
#
#         <!-- Start: sticky menu -->
#         <section class="sticky-menu">
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12">
#                         <nav class="ss-hotel-single-sticky-menu box-shadow-hotel">
#                             <a href="#section-option" class="active-anchor">امکانات هتل</a>
#                                                             <a href="#section-distance" class="">فاصله تا اماکن</a>
#                                                         <a href="#section-info" class="">اطلاعات هتل</a>
#                                                                                                                     <a href="#section-comments" class="">نظرات مسافران</a>
#                                                             <a href="#section-lecture" class="">قلم مسافران</a>
#                                                     </nav>
#                     </div>
#                 </div>
#             </div>
#         </section>
#         <!-- Ends: sticky menu -->
#         <!-- Start: option -->
#         <section id="section-option" class="section">
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12">
#                         <h3 class="ss-innerpage-head-title">
#                             <i>
#                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M488 256.1H80V69.36c0-8.623 5.25-16.37 13.12-19.62c8-3.25 17.12-1.5 23.12 4.623l3.162 3.162C106.4 84.63 110.9 117.1 133.4 140.5l14.84 14.85c-5.936 9.285-5.281 21.56 2.834 29.67C155.7 189.7 161.9 192 168 192s12.28-2.344 16.97-7.031l96-96c9.375-9.375 9.375-24.56 0-33.94c-4.562-4.562-10.44-6.768-16.36-6.766c-4.609 0-9.246 1.334-13.31 3.932L236.5 37.35C213.1 14.86 180.5 10.42 153.4 23.49L151.9 22.01C136.4 6.529 114.8-2.289 93.04 .5156C57.11 5.158 32 35.21 32 69.36v186.7L24 256.1c-13.25 0-24 10.71-24 23.96s10.75 24.02 24 24.02H32v79.96c0 27.12 11.75 52.97 32 71.09v32.9C64 501.3 74.75 512 88 512s24-10.74 24-23.99v-9.623c5.25 1 10.62 1.495 16 1.62h256c5.375-.125 10.75-.6198 16-1.62v9.623C400 501.3 410.7 512 424 512S448 501.3 448 488v-32.9c20.25-18.12 32-43.97 32-71.09V304.1h8c13.25 0 24-10.77 24-24.02S501.3 256.1 488 256.1zM202.5 71.29l14.13 14.13L181.4 120.6L167.3 106.5C157.6 96.8 157.6 81 167.3 71.29C177 61.57 192.8 61.55 202.5 71.29zM432 384c0 26.49-21.5 47.99-48 47.99H128c-26.5 0-48-21.49-48-47.99V304.1h352V384z"/>
#                                 </svg>
#                             </i>امکانات هتل
#                         </h3>
#                         <div class="ss-hotel-single-options-box">
#                             <ul class="ss-hotel-single-options-list">
#                                                                         <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M576 0H64C28.65 0 0 28.65 0 64v320c0 35.35 28.65 64 64 64h512c35.35 0 64-28.65 64-64V64C640 28.65 611.3 0 576 0zM608 384c0 17.64-14.36 32-32 32H64c-17.64 0-32-14.36-32-32V64c0-17.64 14.36-32 32-32h512c17.64 0 32 14.36 32 32V384zM528 480h-416C103.2 480 96 487.2 96 496C96 504.8 103.2 512 112 512h416c8.838 0 16-7.164 16-16C544 487.2 536.8 480 528 480z"/></svg>                                            </i>
#                                             <span>تلویزیون</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M556.2 400.2c-20.89-3.732-41.84-15.52-59-33.22c-9.031-9.312-25.38-9.312-34.41 0C442.6 387.9 413.8 399.8 384 399.8s-58.56-11.98-78.8-32.85c-9.031-9.312-25.38-9.312-34.41 0C250.6 387.9 221.8 399.8 192 399.8c-32.36 0-68.04-13.52-86.79-32.85c-9.031-9.312-25.38-9.312-34.41 0c-19.14 19.76-31.66 29.78-51 33.22c-13.05 2.32-21.75 14.83-19.42 27.92c2.312 13.08 14.66 21.83 27.83 19.49c26.19-4.672 44.73-16.76 61-31.44c28 19.74 66.05 31.81 102.8 31.81c34.89 0 68.76-11.54 95.95-32.19c54.31 41.25 137.4 41.31 191.8 .1582c20.61 16.37 44.16 27.41 68 31.65c1.422 .252 2.844 .377 4.234 .377c11.41 0 21.53-8.199 23.59-19.87C577.1 415 569.2 402.5 556.2 400.2zM556.2 256.2c-20.89-3.732-41.84-15.52-59-33.22c-9.031-9.312-25.38-9.312-34.41 0C442.6 243.9 413.8 255.8 384 255.8s-58.56-11.98-78.8-32.85c-9.031-9.312-25.38-9.312-34.41 0C250.6 243.9 221.8 255.8 192 255.8c-32.36 0-68.04-13.52-86.79-32.85c-9.031-9.312-25.38-9.312-34.41 0c-19.14 19.76-31.66 29.78-51 33.22c-13.05 2.32-21.75 14.83-19.42 27.92c2.312 13.08 14.66 21.83 27.83 19.49c26.19-4.672 44.73-16.76 61-31.44c28 19.74 66 31.69 102.8 31.69c34.89 0 68.81-11.42 95.99-32.07c54.31 41.25 137.4 41.31 191.8 .1582c20.61 16.37 44.16 27.41 68 31.65c1.422 .252 2.844 .377 4.234 .377c11.41 0 21.53-8.199 23.59-19.87C577.1 271 569.2 258.5 556.2 256.2zM28.21 159.6c26.19-4.672 44.73-16.76 61-31.44c28 19.74 66 31.69 102.8 31.69c34.89 0 68.81-11.42 95.99-32.07c54.31 41.25 137.4 41.31 191.8 .1582c20.61 16.37 44.16 27.41 68 31.65c1.422 .252 2.844 .377 4.234 .377c11.41 0 21.53-8.199 23.59-19.87c2.328-13.09-6.375-25.6-19.42-27.92c-20.89-3.732-41.84-15.52-59-33.22c-9.031-9.312-25.38-9.312-34.41 0c-20.23 20.87-48.88 32.94-78.72 32.94s-58.64-12.07-78.87-32.94c-9.031-9.312-25.38-9.312-34.41 0C250.6 99.85 221.9 111.9 192.1 111.9c-32.36 0-68.12-13.61-86.87-32.94c-9.031-9.312-25.38-9.312-34.41 0c-19.14 19.76-31.66 29.78-51 33.22c-13.05 2.32-21.75 14.83-19.42 27.92C2.689 153.2 15.03 161.1 28.21 159.6z"/></svg>                                            </i>
#                                             <span>استخر</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M344 144C344 130.7 354.7 120 368 120C381.3 120 392 130.7 392 144C392 157.3 381.3 168 368 168C354.7 168 344 157.3 344 144zM336 352C326.5 352 317.2 351.3 308.1 349.8L280.1 376.1C276.5 381.5 270.4 384 264 384H224V424C224 437.3 213.3 448 200 448H160V488C160 501.3 149.3 512 136 512H24C10.75 512 0 501.3 0 488V392C0 385.6 2.529 379.5 7.029 375L164.9 217.2C161.7 203.1 160 190.2 160 176C160 78.8 238.8 0 336 0C433.2 0 512 78.8 512 176C512 273.2 433.2 352 336 352zM336 320C415.5 320 480 255.5 480 176C480 96.47 415.5 32 336 32C256.5 32 192 96.47 192 176C192 187.7 193.4 198.1 195.1 209.7L200.1 227.2L32 395.3V480H128V416H192V352H260.7L297 315.6L313.2 318.2C320.6 319.4 328.2 320 336 320V320z"/></svg>                                            </i>
#                                             <span>سوئیت</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M208 72C208 58.75 218.7 48 232 48H248C261.3 48 272 58.75 272 72C272 85.25 261.3 96 248 96H232C218.7 96 208 85.25 208 72zM208 152C208 138.7 218.7 128 232 128H248C261.3 128 272 138.7 272 152C272 165.3 261.3 176 248 176H232C218.7 176 208 165.3 208 152zM16 232C16 218.7 26.75 208 40 208H56C69.26 208 80 218.7 80 232C80 245.3 69.26 256 56 256H40C26.75 256 16 245.3 16 232zM16 315.4C16 300.3 28.28 288 43.43 288H532.6C547.7 288 560 300.3 560 315.4C560 388.3 512.6 450.2 446.9 471.8C447.6 474.4 448 477.2 448 480C448 497.7 433.7 512 416 512H160C142.3 512 128 497.7 128 480C128 477.2 128.4 474.4 129.1 471.8C63.4 450.2 16 388.3 16 315.4L16 315.4zM176.4 464H399.6C402.4 446.9 414.4 431.9 431.9 426.2C472.2 412.9 502.6 378.4 510.2 336H65.81C73.36 378.4 103.8 412.9 144.1 426.2C161.6 431.9 173.6 446.9 176.4 464H176.4zM248 208C261.3 208 272 218.7 272 232C272 245.3 261.3 256 248 256H232C218.7 256 208 245.3 208 232C208 218.7 218.7 208 232 208H248zM152 208C165.3 208 176 218.7 176 232C176 245.3 165.3 256 152 256H136C122.7 256 112 245.3 112 232C112 218.7 122.7 208 136 208H152zM112 152C112 138.7 122.7 128 136 128H152C165.3 128 176 138.7 176 152C176 165.3 165.3 176 152 176H136C122.7 176 112 165.3 112 152zM344 208C357.3 208 368 218.7 368 232C368 245.3 357.3 256 344 256H328C314.7 256 304 245.3 304 232C304 218.7 314.7 208 328 208H344zM304 152C304 138.7 314.7 128 328 128H344C357.3 128 368 138.7 368 152C368 165.3 357.3 176 344 176H328C314.7 176 304 165.3 304 152zM440 208C453.3 208 464 218.7 464 232C464 245.3 453.3 256 440 256H424C410.7 256 400 245.3 400 232C400 218.7 410.7 208 424 208H440zM400 152C400 138.7 410.7 128 424 128H440C453.3 128 464 138.7 464 152C464 165.3 453.3 176 440 176H424C410.7 176 400 165.3 400 152zM536 208C549.3 208 560 218.7 560 232C560 245.3 549.3 256 536 256H520C506.7 256 496 245.3 496 232C496 218.7 506.7 208 520 208H536zM344 48C357.3 48 368 58.75 368 72C368 85.25 357.3 96 344 96H328C314.7 96 304 85.25 304 72C304 58.75 314.7 48 328 48H344z"/></svg>                                            </i>
#                                             <span>رستوران</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M319.1 367.1C289.1 367.1 264 393.1 264 424s25.07 56 55.1 56S376 454.9 376 424S350.9 367.1 319.1 367.1zM632.5 150.6C553.3 75.22 439.4 32 320 32S86.72 75.22 7.473 150.6c-9.625 9.125-10 24.31-.8438 33.91c9.062 9.594 24.31 10 33.91 .8438C110.1 118.4 212.8 80 320 80s209 38.41 279.5 105.4C604.1 189.8 610.1 192 615.1 192c6.344 0 12.69-2.5 17.38-7.469C642.5 174.9 642.2 159.8 632.5 150.6zM320 207.9c-76.63 0-147.9 28-200.6 78.75C109.8 295.9 109.5 311.1 118.7 320.6c9.219 9.625 24.41 9.844 33.94 .6875C196.4 279.2 255.8 256 320 256s123.6 23.19 167.4 65.31C492 325.8 497.1 328 503.1 328c6.281 0 12.59-2.469 17.31-7.375c9.188-9.531 8.875-24.72-.6875-33.94C467.9 235.9 396.6 207.9 320 207.9z"/></svg>                                            </i>
#                                             <span>اینترنت</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M176 80H128C119.2 80 112 87.16 112 96S119.2 112 128 112h48C184.8 112 192 104.8 192 96S184.8 80 176 80zM424 48C437.3 48 448 37.25 448 24S437.3 0 424 0H24C10.75 0 0 10.75 0 24S10.75 48 24 48H32v164.1C17.04 224.8 8 239 8 256c0 51.01 24.52 97.21 64 130.6V472C72 494.1 89.94 512 112 512h224c22.06 0 40-17.94 40-40v-85.44c39.48-33.36 64-79.55 64-130.6c0-16.96-9.035-31.15-24-43.04V48H424zM80 48h288v140.4C327.4 174.6 274.8 168 224 168S120.6 174.6 80 188.4V48zM328 464h-208v-46.82C150.9 431.7 186.3 440 224 440s73.12-8.309 104-22.82V464zM224 392c-62.26 0-116.1-27.88-145.1-68.72C119.7 337.3 172.8 344 224 344s104.3-6.717 145.1-20.72C340.1 364.1 286.3 392 224 392zM224 296c-107.5 0-164.1-29.17-167.9-39.54c-.002-.1055 0 .1055 0 0C59.75 245.2 116.4 216 224 216c106.6 0 163.2 28.53 167.9 40C387.2 267.5 330.6 296 224 296z"/></svg>                                            </i>
#                                             <span>سرویس فرنگی</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M463.1 144c-13.25 0-23.1 21.5-23.1 48s10.75 48 23.1 48s24-21.5 24-48S477.2 144 463.1 144zM463.1 0H143.1C82.1 0 31.98 86 31.98 192v172.1c0 41.12-9.751 62.75-31.13 126.9C-2.65 501.2 5.101 512 15.98 512h328.9c13.88 0 26-8.75 30.38-21.88c11.25-33.5 21.63-63.5 24.13-106.1h64.63C525.9 384 576 298 576 192C576 86 525.9 0 463.1 0zM351.1 192l-.0044 172.1c0 41-8 68-18.63 99.88H60.6c12.5-37.5 19.38-62.25 19.38-99.88V192c0-86.62 38.5-144 64-144h246.1C366.7 83.25 351.1 134.6 351.1 192zM463.1 336c-25.5 0-64-57.38-64-144s38.5-144 64-144s64 57.38 64 144S489.5 336 463.1 336zM207.1 223.1c8.829 0 15.1-7.157 15.1-15.99S216.8 192 207.1 192C199.2 192 191.1 199.2 191.1 207.1S199.2 223.1 207.1 223.1zM272 224c8.83 0 15.99-7.169 15.99-15.1S280.8 192 272 192S255.1 199.2 255.1 208S263.2 224 272 224zM127.1 207.1c0 8.833 7.175 15.1 16.01 15.1s15.99-7.166 15.99-15.1C159.1 199.2 152.8 192 144 192S127.1 199.2 127.1 207.1z"/></svg>                                            </i>
#                                             <span>سرویس ایرانی</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M70.02 47.78C80.26 19.13 107.4 0 137.8 0H278.2C308.6 0 335.7 19.13 345.1 47.78L374.6 127.9L374.6 127.1H361.8C332.9 127.1 305.1 139.1 286.8 159.1H96C69.49 159.1 48 181.5 48 207.1V239.1H248.5L237.9 269.8C231.4 275.3 225.4 281.4 220.1 287.1H48V328C48 341.3 37.25 352 24 352C10.75 352 0 341.3 0 328V207.1C0 175.5 16.18 146.7 40.94 129.3C41.08 128.9 41.23 128.4 41.4 127.9L70.02 47.78zM137.8 48C127.7 48 118.6 54.38 115.2 63.93L98.06 112H317.9L300.8 63.93C297.4 54.38 288.3 48 278.2 48H137.8zM88 200C88 186.7 98.75 176 112 176C125.3 176 136 186.7 136 200C136 213.3 125.3 224 112 224C98.75 224 88 213.3 88 200zM312 360C312 346.7 322.7 336 336 336C349.3 336 360 346.7 360 360C360 373.3 349.3 384 336 384C322.7 384 312 373.3 312 360zM552 360C552 373.3 541.3 384 528 384C514.7 384 504 373.3 504 360C504 346.7 514.7 336 528 336C541.3 336 552 346.7 552 360zM294 207.8C304.3 179.1 331.4 160 361.8 160H502.2C532.6 160 559.7 179.1 569.1 207.8L598.6 287.9C598.8 288.4 598.9 288.9 599.1 289.3C623.8 306.7 640 335.5 640 368V488C640 501.3 629.3 512 616 512C602.7 512 592 501.3 592 488V448H272V488C272 501.3 261.3 512 248 512C234.7 512 224 501.3 224 488V368C224 335.5 240.2 306.7 264.9 289.3C265.1 288.9 265.2 288.4 265.4 287.9L294 207.8zM361.8 208C351.7 208 342.6 214.4 339.2 223.9L322.1 272H541.9L524.8 223.9C521.4 214.4 512.3 208 502.2 208H361.8zM544 320H320C293.5 320 272 341.5 272 368V400H592V368C592 341.5 570.5 320 544 320z"/></svg>                                            </i>
#                                             <span>پارکینگ</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M400 .0006C407.6 .0006 414.7 3.557 419.2 9.601C437.2 33.59 459.3 51.71 485.7 69.06C501.3 79.39 516.1 88.52 533.9 98.39C546.9 106 560.8 114.1 576 123.6C606.1 142.8 624 176.8 624 211.8C624 237.5 615.1 261 600.2 279.6C623.8 291.4 640 315.8 640 344V440C640 479.8 607.8 512 568 512H72C32.24 512 0 479.8 0 440V140.7C0 96.25 20.52 54.31 55.59 27.02L81.27 7.056C89.93 .3149 102.1 .3149 110.7 7.056L136.4 27.02C163.3 47.94 181.6 77.46 188.7 110.1C164.6 131.7 149.8 161.1 145.4 192H48V440C48 453.3 58.75 464 72 464H164.1C161.4 456.5 160 448.4 160 440V344C160 315.8 176.2 291.4 199.8 279.6C184.9 261 176 237.5 176 211.8C176 176.8 193 142.8 223.1 123.6C239.2 114.1 253.1 106 266.1 98.39C283 88.52 298.7 79.39 314.4 69.06C340.7 51.71 362.8 33.59 380.8 9.6C385.3 3.557 392.4 0 400 0L400 .0006zM232 464H256V408C256 394.7 266.7 384 280 384C293.3 384 304 394.7 304 408V464H352V413.1C352 394.1 360.4 376.1 375 364.8L400 344L424.1 364.8C439.6 376.1 448 394.1 448 413.1V464H496V408C496 394.7 506.7 384 520 384C533.3 384 544 394.7 544 408V464H568C581.3 464 592 453.3 592 440V344C592 330.7 581.3 320 568 320H232C218.7 320 208 330.7 208 344V440C208 453.3 218.7 464 232 464zM48 144H144V140.7C144 111.1 130.3 83.1 106.9 64.91L96 56.41L85.06 64.91C61.68 83.1 48 111.1 48 140.7V144zM550.7 164.4C538.1 156.5 524.8 148.8 511.7 141.1C493.4 130.3 475.2 119.7 459.3 109.2C438.2 95.28 418.1 79.98 400 61.04C381.9 79.98 361.8 95.28 340.7 109.2C324.8 119.7 306.6 130.3 288.3 141.1C275.2 148.8 261.9 156.5 249.3 164.4C233.6 174.1 224 191.1 224 211.8C224 245.1 250.9 272 284.2 272H515.8C549.1 272 576 245.1 576 211.8C576 191.1 566.4 174.1 550.7 164.4z"/></svg>                                            </i>
#                                             <span>نمازخانه</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M624.3 18.08C627.4 19.41 630.3 21.36 632.6 23.79C635 26.23 636.9 29.11 638.2 32.27C639.4 35.43 640 38.81 640 42.21V480C640 484.2 638.3 488.3 635.3 491.3C632.3 494.3 628.2 496 624 496C619.8 496 615.7 494.3 612.7 491.3C609.7 488.3 608 484.2 608 480V320H562.9C556.1 319.9 549.4 318.5 543.2 315.8C536.9 313.1 531.2 309.1 526.5 304.2C521.8 299.3 518.1 293.6 515.6 287.2C513.1 280.9 511.9 274.1 512 267.3L512.4 158.2C512.2 128.3 520.8 99 537.3 74.03C553.7 49.05 577.2 29.51 604.8 17.89C607.8 16.64 611.1 16 614.4 16C617.8 16.04 621.2 16.74 624.3 18.08V18.08zM608 51.78C588.7 61.98 572.5 77.32 561.4 96.09C550.2 114.9 544.4 136.4 544.6 158.2L544 267.5C543.1 270.3 544.5 273 545.5 275.6C546.6 278.2 548.2 280.5 550.1 282.5C551.8 284.2 553.8 285.6 555.1 286.5C558.2 287.5 560.6 287.1 562.9 288H608V51.78zM145.9 209.9C136.9 218.9 124.7 224 112 224H96V480C96 484.2 94.31 488.3 91.31 491.3C88.31 494.3 84.24 496 80 496C75.76 496 71.69 494.3 68.69 491.3C65.69 488.3 64 484.2 64 480V224H48C35.27 224 23.06 218.9 14.06 209.9C5.057 200.9 0 188.7 0 176V32C0 27.76 1.686 23.69 4.686 20.69C7.687 17.69 11.76 16 16 16C20.24 16 24.31 17.69 27.31 20.69C30.31 23.69 32 27.76 32 32V176C32 180.2 33.69 184.3 36.69 187.3C39.69 190.3 43.76 192 48 192H64V32C64 27.76 65.69 23.69 68.69 20.69C71.69 17.69 75.76 16 80 16C84.24 16 88.31 17.69 91.31 20.69C94.31 23.69 96 27.76 96 32V192H112C116.2 192 120.3 190.3 123.3 187.3C126.3 184.3 128 180.2 128 176V32C128 27.76 129.7 23.69 132.7 20.69C135.7 17.69 139.8 16 144 16C148.2 16 152.3 17.69 155.3 20.69C158.3 23.69 160 27.76 160 32V176C160 188.7 154.9 200.9 145.9 209.9zM437.8 154.2C464.8 181.2 480 217.8 480 256C480 284.5 471.6 312.3 455.7 336C439.9 359.7 417.4 378.1 391.1 389C364.8 399.9 335.8 402.8 307.9 397.2C279.1 391.7 254.3 377.1 234.2 357.8C214 337.7 200.3 312 194.8 284.1C189.2 256.2 192.1 227.2 202.1 200.9C213.9 174.6 232.3 152.1 255.1 136.3C279.7 120.4 307.5 112 336 112C374.2 112 410.8 127.2 437.8 154.2L437.8 154.2zM415.2 335.2C436.2 314.2 448 285.7 448 256C448 233.9 441.4 212.2 429.1 193.8C416.8 175.4 399.3 161 378.9 152.5C358.4 144.1 335.9 141.8 314.1 146.2C292.4 150.5 272.5 161.1 256.8 176.8C241.1 192.5 230.5 212.4 226.2 234.2C221.8 255.9 224 278.4 232.5 298.9C241 319.3 255.4 336.8 273.8 349.1C292.2 361.4 313.8 368 336 368C365.7 368 394.2 356.2 415.2 335.2zM542.7 358.2C544 359.9 544.1 361.8 545.5 363.8C546.1 365.9 546.2 367.1 545.1 370.1C545.7 372.2 545 374.2 544 376C522.1 413.9 490.3 445.1 451.9 466.2C413.6 487.3 370.2 497.5 326.5 495.7C282.8 493.1 240.4 480.3 203.9 456.2C167.4 432.1 138.2 398.4 119.4 358.9C118.3 356.1 117.6 354.9 117.4 352.7C117.2 350.5 117.4 348.3 118 346.2C118.7 344.1 119.8 342.1 121.2 340.5C122.7 338.8 124.4 337.5 126.4 336.5C128.4 335.6 130.5 335.1 132.7 334.1C134.9 334.9 137.1 335.3 139.2 336.1C141.2 336.9 143.1 338.1 144.6 339.7C146.2 341.2 147.4 343.1 148.2 345.1C164.5 379.4 189.8 408.5 221.4 429.5C253 450.4 289.8 462.2 327.7 463.8C365.6 465.3 403.2 456.4 436.4 438.2C469.6 419.9 497.2 392.8 516.2 360C518.3 356.3 521.8 353.7 525.9 352.6C529.1 351.5 534.3 352 538 354.1C539.8 355.2 541.5 356.6 542.7 358.2V358.2zM195.5 95.9C191.3 95.4 187.5 93.24 184.8 89.91C182.2 86.57 181 82.33 181.5 78.11C182 73.9 184.2 70.05 187.5 67.43C229.8 34.1 282.1 15.98 336 15.98C389.9 15.98 442.2 34.1 484.5 67.43C487.8 70.05 489.1 73.9 490.5 78.11C490.1 82.33 489.8 86.57 487.2 89.91C484.5 93.24 480.7 95.4 476.5 95.9C472.2 96.4 468 95.21 464.7 92.58C427.8 64.23 382.5 48.86 336 48.86C289.5 48.86 244.2 64.23 207.3 92.58C203.1 95.21 199.8 96.4 195.5 95.9z"/></svg>                                            </i>
#                                             <span>لابی</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M201.5 344.5l47.48-47.48c9.375-9.375 9.375-24.56 0-33.94s-24.56-9.375-33.94 0L167.5 310.5L72.06 215C67.11 210.1 60.33 207.7 53.27 208.1C46.3 208.6 39.89 212.2 35.75 217.8C12.36 249.7 0 287.4 0 327.1C0 429.1 82.95 512 184.9 512c39.66 0 77.45-12.38 109.3-35.75c5.641-4.156 9.203-10.53 9.734-17.53c.5313-6.969-2.016-13.84-6.969-18.78L201.5 344.5zM184.9 464C109.4 464 48 402.6 48 327.1c0-19.66 4.109-38.72 12.02-56.22L241.1 452C223.6 459.9 204.6 464 184.9 464zM216 0C202.8 0 192 10.75 192 24S202.8 48 216 48c136.8 0 248 111.3 248 248c0 13.25 10.75 24 24 24S512 309.3 512 296C512 132.8 379.2 0 216 0zM216 104C202.8 104 192 114.8 192 128s10.75 24 24 24c79.41 0 144 64.59 144 144C360 309.3 370.8 320 384 320s24-10.75 24-24C408 190.1 321.9 104 216 104z"/></svg>                                            </i>
#                                             <span>ماهواره</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M608 224V152C608 121.1 582.9 96 552 96h-32C517.3 96 514.6 96.38 512 96.75V88C512 57.07 486.9 32 456 32h-32c-30.93 0-56 25.07-56 56V224h-96V88C272 57.07 246.9 32 216 32h-32C153.1 32 128 57.07 128 88v8.75C125.4 96.38 122.8 96 120 96h-32C57.07 96 32 121.1 32 152V224C14.4 224 0 238.4 0 256s14.4 32 31.1 32L32 360C32 390.9 57.07 416 88 416h32c2.75 0 5.375-.375 8-.75V424C128 454.9 153.1 480 184 480h32c30.93 0 56-25.07 56-56V288h96v136c0 30.93 25.07 56 56 56h32c30.93 0 56-25.07 56-56v-8.75C514.6 415.6 517.3 416 520 416h32c30.93 0 56-25.07 56-56V288c17.6 0 32-14.4 32-32S625.6 224 608 224zM120 368h-32c-4.375 0-8-3.625-8-8v-208c0-4.375 3.625-8 8-8h32C124.4 144 128 147.6 128 152v208C128 364.4 124.4 368 120 368zM224 424c0 4.375-3.625 8-8 8h-32c-4.375 0-8-3.625-8-8V88c0-4.375 3.625-8 8-8h32C220.4 80 224 83.62 224 88V424zM464 424c0 4.375-3.625 8-8 8h-32c-4.375 0-8-3.625-8-8V88c0-4.375 3.625-8 8-8h32c4.375 0 8 3.625 8 8V424zM560 360c0 4.375-3.625 8-8 8h-32c-4.375 0-8-3.625-8-8v-208c0-4.375 3.625-8 8-8h32c4.375 0 8 3.625 8 8V360z"/></svg>                                            </i>
#                                             <span>سالن ورزش</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M.0003 185.8C.0003 179.4 1.606 173.1 4.67 167.4L82.36 25.02C90.77 9.595 106.9 0 124.5 0H515.5C533.1 0 549.2 9.595 557.6 25.02L635.3 167.4C638.4 173.1 640 179.4 640 185.8C640 206.9 622.9 224 601.8 224H576V488C576 501.3 565.3 512 552 512C538.7 512 528 501.3 528 488V224H384V472C384 494.1 366.1 512 344 512H103.1C81.91 512 63.1 494.1 63.1 472V224H38.25C17.12 224 0 206.9 0 185.8H.0003zM111.1 224V320H336V224H111.1zM124.5 48L54.68 176H585.3L515.5 48H124.5zM336 464V368H111.1V464H336z"/></svg>                                            </i>
#                                             <span>فروشگاه و غرفه</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M480 192H32c-17.62 0-32 14.37-32 31.1c0 94.75 51.5 177.1 128 221.5v34.5c0 17.62 14.38 31.1 32 31.1h192c17.62 0 32-14.37 32-31.1v-34.5c76.5-44.38 128-126.7 128-221.5C512 206.4 497.6 192 480 192zM336 417.8v46.25h-160v-46.25c-67.5-39.13-120.3-87-127.4-177.8h414.8C456.4 328.9 405.4 377.6 336 417.8zM171.9 100.7C184.3 107.1 192 121.4 192 136c0 13.25 10.75 23.89 24 23.89S240 148.1 240 135.7c0-31.34-16.81-60.64-43.91-76.45C183.7 52.03 176 38.63 176 24.28c0-13.25-10.75-24.14-24-24.14S128 11.03 128 24.28C128 55.63 144.8 84.92 171.9 100.7zM283.9 100.7C296.3 107.1 304 121.4 304 136c0 13.25 10.75 23.86 24 23.86S352 148.1 352 135.7c0-31.34-16.81-60.64-43.91-76.45C295.7 52.03 288 38.63 288 24.28c0-13.25-10.75-24.18-24-24.18S240 11.03 240 24.28C240 55.63 256.8 84.92 283.9 100.7z"/></svg>                                            </i>
#                                             <span>کافی شاپ</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M319.1 367.1C289.1 367.1 264 393.1 264 424s25.07 56 55.1 56S376 454.9 376 424S350.9 367.1 319.1 367.1zM632.5 150.6C553.3 75.22 439.4 32 320 32S86.72 75.22 7.473 150.6c-9.625 9.125-10 24.31-.8438 33.91c9.062 9.594 24.31 10 33.91 .8438C110.1 118.4 212.8 80 320 80s209 38.41 279.5 105.4C604.1 189.8 610.1 192 615.1 192c6.344 0 12.69-2.5 17.38-7.469C642.5 174.9 642.2 159.8 632.5 150.6zM320 207.9c-76.63 0-147.9 28-200.6 78.75C109.8 295.9 109.5 311.1 118.7 320.6c9.219 9.625 24.41 9.844 33.94 .6875C196.4 279.2 255.8 256 320 256s123.6 23.19 167.4 65.31C492 325.8 497.1 328 503.1 328c6.281 0 12.59-2.469 17.31-7.375c9.188-9.531 8.875-24.72-.6875-33.94C467.9 235.9 396.6 207.9 320 207.9z"/></svg>                                            </i>
#                                             <span>اینترنت در لابی</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M256 192C242.8 192 232 202.8 232 216S242.8 240 256 240s24-10.78 24-24S269.2 192 256 192zM256 160c8.828 0 16-7.188 16-16S264.8 128 256 128S240 135.2 240 144S247.2 160 256 160zM256 64C185.3 64 128 121.3 128 192c0 70.69 57.31 128 128 128s128-57.31 128-128C384 121.3 326.7 64 256 64zM256 272c-30.88 0-56-25.12-56-56c0-16.66 7.459-31.48 19.04-41.74C212.3 165.1 208 155.5 208 144C208 117.5 229.5 96 256 96s48 21.53 48 48c0 11.53-4.25 21.97-11.04 30.26C304.5 184.5 312 199.3 312 216C312 246.9 286.9 272 256 272zM256 0C114.6 0 0 114.6 0 256s114.6 256 256 256s256-114.6 256-256S397.4 0 256 0zM256 464c-114.7 0-208-93.31-208-208S141.3 48 256 48s208 93.31 208 208S370.7 464 256 464z"/></svg>                                            </i>
#                                             <span>بیلیارد</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M480.3 320.3L382.1 278.2c-21.41-9.281-46.64-3.109-61.2 14.95l-27.44 33.5c-44.78-25.75-82.29-63.25-108-107.1l33.55-27.48c17.91-14.62 24.09-39.7 15.02-61.05L191.7 31.53c-10.16-23.2-35.34-35.86-59.87-30.19l-91.25 21.06C16.7 27.86 0 48.83 0 73.39c0 241.9 196.7 438.6 438.6 438.6c24.56 0 45.53-16.69 50.1-40.53l21.06-91.34C516.4 355.5 503.6 330.3 480.3 320.3zM463.9 369.3l-21.09 91.41c-.4687 1.1-2.109 3.281-4.219 3.281c-215.4 0-390.6-175.2-390.6-390.6c0-2.094 1.297-3.734 3.344-4.203l91.34-21.08c.3125-.0781 .6406-.1094 .9531-.1094c1.734 0 3.359 1.047 4.047 2.609l42.14 98.33c.75 1.766 .25 3.828-1.25 5.062L139.8 193.1c-8.625 7.062-11.25 19.14-6.344 29.14c33.01 67.23 88.26 122.5 155.5 155.5c9.1 4.906 22.09 2.281 29.16-6.344l40.01-48.87c1.109-1.406 3.187-1.938 4.922-1.125l98.26 42.09C463.2 365.2 464.3 367.3 463.9 369.3z"/></svg>                                            </i>
#                                             <span>تلفن در اتاق</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M575.1 455.9c0-11.45-8.176-21.6-19.8-23.67C508.7 423.7 502.3 392 479.1 392c-22.91 0-33.8 39.83-95.1 39.83c-62.23 0-73.08-39.83-96-39.83c-22.92 0-33.77 39.83-96 39.83c-69.59 0-81.1-39.83-103.1-39.83c-21.95 0-30.18 33.43-68.2 40.21c-11.62 2.067-19.8 12.22-19.8 23.67c0 12.1 9.506 24.12 23.94 24.12c7.637 0 35.43-4.889 65.27-31.81c28 19.74 66.04 31.81 102.8 31.81c34.89 0 68.77-11.54 95.96-32.19c27.19 20.65 61.6 30.98 96.01 30.98c34.32 0 68.63-10.27 95.78-30.82c30.59 24.3 63.21 32.03 72.23 32.03C563.1 479.1 575.1 470.4 575.1 455.9zM480 32C427.1 32 384 75.06 384 128v96H176V128c0-26.47 21.53-48 48-48S272 101.5 272 128v8C272 149.3 282.8 160 296 160S320 149.3 320 136V128c0-52.94-43.06-95.1-96-95.1S128 75.06 128 128v232C128 373.3 138.8 384 152 384s24-10.75 24-24V272H384v88c0 13.25 10.75 24 24 24s24-10.75 24-24V128c0-26.47 21.53-48 48-48s48 21.53 48 48v8C528 149.3 538.8 160 552 160S576 149.3 576 136V128C576 75.06 532.9 32 480 32z"/></svg>                                            </i>
#                                             <span>سونا و جکوزی</span>
#                                         </li>
#                                                                             <li class="ss-hotel-single-options-item">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M288 0H96C42.98 0 0 42.98 0 96v352c0 35.35 28.65 64 64 64h256c35.35 0 64-28.65 64-64V96C384 42.98 341 0 288 0zM336 448c0 8.822-7.178 16-16 16H64c-8.822 0-16-7.178-16-16V208h192v136c0 13.25 10.75 24 24 24S288 357.3 288 344V208h48V448zM336 160H288V120C288 106.8 277.3 96 264 96S240 106.8 240 120V160h-192V96c0-26.47 21.53-48 48-48h192c26.47 0 48 21.53 48 48V160z"/></svg>                                            </i>
#                                             <span>یخچال</span>
#                                         </li>
#                                                                 </ul>
#                             <h4 class="ss-innerpage-head-title">هتل بزرگ شیراز امکانات زیر را ندارد</h4>
#                             <ul class="ss-hotel-single-options-list">
#                                                                         <li class="ss-hotel-single-options-item disable">
#                                             <i>
#                                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M240 104C240 112.8 232.8 120 223.1 120C215.2 120 207.1 112.8 207.1 104V24C207.1 15.16 215.2 8 223.1 8C232.8 8 240 15.16 240 24V104zM87.1 376C87.1 362.7 98.75 352 111.1 352C125.3 352 135.1 362.7 135.1 376C135.1 389.3 125.3 400 111.1 400C98.75 400 87.1 389.3 87.1 376zM360 376C360 389.3 349.3 400 336 400C322.7 400 312 389.3 312 376C312 362.7 322.7 352 336 352C349.3 352 360 362.7 360 376zM156.2 176H291.8C320.4 176 345.5 194.9 353.3 222.4L374.1 298.1C399.4 311.8 416 337.1 416 368V496C416 504.8 408.8 512 400 512C391.2 512 384 504.8 384 496V464H63.1V496C63.1 504.8 56.84 512 47.1 512C39.16 512 31.1 504.8 31.1 496V368C31.1 337.1 48.56 311.8 73.04 298.1L94.67 222.4C102.5 194.9 127.6 176 156.2 176V176zM156.2 208C141.9 208 129.4 217.5 125.4 231.2L109.2 288C110.1 288 111.1 288 111.1 288H336C336.9 288 337.9 288 338.8 288L322.6 231.2C318.6 217.5 306.1 208 291.8 208H156.2zM384 368C384 341.5 362.5 320 336 320H111.1C85.49 320 63.1 341.5 63.1 368V432H384V368zM12.69 44.69C18.93 38.44 29.06 38.44 35.31 44.69L83.31 92.69C89.56 98.93 89.56 109.1 83.31 115.3C77.07 121.6 66.94 121.6 60.69 115.3L12.69 67.31C6.438 61.07 6.438 50.94 12.69 44.69V44.69zM412.7 44.69C418.9 38.44 429.1 38.44 435.3 44.69C441.6 50.93 441.6 61.07 435.3 67.31L387.3 115.3C381.1 121.6 370.9 121.6 364.7 115.3C358.4 109.1 358.4 98.94 364.7 92.69L412.7 44.69z"/></svg>                                            </i>
#                                             <span>ترانسفر فرودگاهی </span>
#
#                                         </li>
#                                                                 </ul>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         </section>
#         <!-- Ends: option -->
#
#
#
#
#         <!--   fixme:this section will be deleted after data entry     -->
#         <!-- Start: distance -->
#                     <section id="section-distance"  class="section">
#                 <div class="container">
#                     <div class="row">
#                         <div class="col-md-12">
#                             <h3 class="ss-innerpage-head-title">
#                                 <i>
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M408 119.1C408 128.6 406.2 138.3 402.1 148.6C397.3 166.1 387.4 187.5 375.6 207.8L375.5 207.1C372.4 213.3 369.2 218.7 365.9 224C361.5 231 356.9 237.1 352.4 244.8L352 245.4C333.9 272.3 315.3 296.4 302.8 311.1C295.1 321.6 280.9 321.6 273.2 311.1C260.7 296.4 242.1 272.3 224 245.4C205.6 218.1 187.7 187.9 177.3 160.9C176.5 158.8 175.7 156.7 174.1 154.6C170.6 142 168 130.3 168 120C168 115.3 168.3 110.7 168.8 106.2C175.6 46.44 226.4 0 288 0C354.3 0 408 53.73 408 120V119.1zM288 151.1C310.1 151.1 328 134.1 328 111.1C328 89.91 310.1 71.1 288 71.1C265.9 71.1 248 89.91 248 111.1C248 134.1 265.9 151.1 288 151.1zM352 300.6C365.5 282.4 380.8 260.7 394.7 238.2C396.5 235.3 398.2 232.4 400 229.5V453.7L528 407.2V154.3L419.3 193.8C421.5 189.1 423.6 184.5 425.6 179.8C431.5 165.8 436.6 150.7 438.8 135.6L543.8 97.44C551.2 94.77 559.4 95.85 565.8 100.3C572.2 104.8 576 112.2 576 119.1V424C576 434.1 569.7 443.1 560.2 446.6L384.2 510.6C378.9 512.5 373.1 512.5 367.8 510.6L200 449.5L32.2 510.6C24.84 513.2 16.64 512.2 10.23 507.7C3.819 503.2 0 495.8 0 488V183.1C0 173.9 6.314 164.9 15.8 161.4L136 117.7C136 118.5 136 119.2 136 119.1C136 135.1 139.7 150.7 144.9 165.6L48 200.8V453.7L176 407.2V229.5C177.8 232.4 179.5 235.3 181.3 238.2C195.2 260.7 210.5 282.4 224 300.6V407.2L352 453.7V300.6z"/></svg>
#                                 </i>فاصله هتل بزرگ شیراز تا مکان های مهم شهر شیراز                            </h3>
#                             <div class="ss-hotel-single-distance-box">
#                                 <div class="ss-hotel-single-distance-right">
#                                     <div class="ss-hotel-single-dr-list">
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس ارگ کریمخانی" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">ارگ کریمخانی</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">12 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس آرامگاه حافظ (حافظیه)" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">آرامگاه حافظ (حافظیه)</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">5 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس باغ ارم" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">باغ ارم</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">5 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس آرامگاه سعدی" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">آرامگاه سعدی</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">11 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس تخت جمشید" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">تخت جمشید</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">45 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس نمایشگاه بین المللی شیراز" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">نمایشگاه بین المللی شیراز</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">30 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس باغ جهان نما" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">باغ جهان نما</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">10 دقیقه پیاده</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس آرامگاه کوروش" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">آرامگاه کوروش</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">1ساعت و20 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس بازار وکیل" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">بازار وکیل</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">10 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس راه آهن" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">راه آهن</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">25 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس مسجد وکیل" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">مسجد وکیل</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">10 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس آرامگاه شاه چراغ" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">آرامگاه شاه چراغ</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">10 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس فرودگاه بین المللی شیراز" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">فرودگاه بین المللی شیراز</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">23 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس مرکز خرید نگین فارس" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">مرکز خرید نگین فارس</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">25 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس مرکز تجاری خلیج فارس" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">مرکز تجاری خلیج فارس</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">26 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس مرکز خرید آفتاب" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">مرکز خرید آفتاب</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">20 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#                                                                                     <a class="ss-hotel-single-dr-item" >
#                                                 <figure class="ss-hotel-single-dri-figure">
#                                                     <span class="text-off">text off</span>
#                                                                                                         <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" alt="عکس ترمینال مسافربری کاراندیش شیراز" >
#                                                 </figure>
#                                                 <div class="ss-hotel-single-dri-content">
#                                                                                                         <span class="ss-hotel-single-dric-sub">فاصله تا</span>
#                                                     <span class="ss-hotel-single-dric-name">ترمینال مسافربری کاراندیش شیراز</span>
#                                                     <span class="ss-hotel-single-dric-long">
#                                                                                                 <span class="color-gray">10 دقیقه با ماشین</span>
#                                                                                         </span>
#                                                 </div>
#                                             </a>
#
#
#
#                                     </div>
#                                 </div>
#                             </div>
#                         </div>
#                     </div>
#                 </div>
#             </section>
#                 <!-- Ends: distance -->
#         <!--   fixme:this section will be deleted after data entry     -->
#
#
#         <!-- Start: info -->
#         <section id="section-info"  class="section">
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12">
#                         <h3 class="ss-innerpage-head-title">
#                             <i>
#                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256s256-114.6 256-256S397.4 0 256 0zM256 464c-114.7 0-208-93.31-208-208S141.3 48 256 48s208 93.31 208 208S370.7 464 256 464zM296 336h-16V248C280 234.8 269.3 224 256 224H224C210.8 224 200 234.8 200 248S210.8 272 224 272h8v64h-16C202.8 336 192 346.8 192 360S202.8 384 216 384h80c13.25 0 24-10.75 24-24S309.3 336 296 336zM256 192c17.67 0 32-14.33 32-32c0-17.67-14.33-32-32-32S224 142.3 224 160C224 177.7 238.3 192 256 192z"/></svg>
#                             </i>اطلاعات و راهنما رزرو هتل بزرگ شیراز:
#                         </h3>
#                         <div class="ss-hotel-single-info-box">
#                             <p class="text-justify">هتل بزرگ شیراز در آبان ماه 1392 با زیربنای 40 هزار متر مربع به بهره برداری رسید. این هتل بر فراز کوه های شمال شرقی شیراز در 14 طبقه بنا شده است. هتل بزرگ با نام دروازه قرآن نیز شناخته می شود. این هتل برای پذیرایی از مهمانان و گردشگرانی که شیراز را مقصد سفر خود برگزیده اند دارای 158 باب اتاق با امکانات کامل اقامتی می باشد که در طبقات هفتم تا دوازدهم واقع شده اند. هتل پنج ستاره بزرگ شیراز از هتل های مجهز در شیراز به شمار می رود که با اقامت در این هتل و پیمودن فاصله ای حدودا 3 کیلومتر، می توان از آرامگاه خواجوی کرمانی نیز دیدن کرد.
#
#                             </p>
#                                                     </div>
#                     </div>
#                 </div>
#             </div>
#         </section>
#         <!-- Ends: info -->
#         <!-- Start: comments -->
#         <section id="section-comments">
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12">
#                         <h3 class="ss-innerpage-head-title">
#                             <i>
#                                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M360 144h-208C138.8 144 128 154.8 128 168S138.8 192 152 192h208C373.3 192 384 181.3 384 168S373.3 144 360 144zM264 240h-112C138.8 240 128 250.8 128 264S138.8 288 152 288h112C277.3 288 288 277.3 288 264S277.3 240 264 240zM447.1 0h-384c-35.25 0-64 28.75-64 63.1v287.1c0 35.25 28.75 63.1 64 63.1h96v83.1c0 9.836 11.02 15.55 19.12 9.7l124.9-93.7h144c35.25 0 64-28.75 64-63.1V63.1C511.1 28.75 483.2 0 447.1 0zM464 352c0 8.75-7.25 16-16 16h-160l-80 60v-60H64c-8.75 0-16-7.25-16-16V64c0-8.75 7.25-16 16-16h384c8.75 0 16 7.25 16 16V352z"/></svg>
#                             </i>نظرات مسافران در مورد  هتل بزرگ شیراز                        </h3>
#                         <div class="ss-hotel-single-comments-wrapper" id="comments-container">
#                                                                 <div class="ss-hotel-single-comments-item">
#                                         <div class="ss-hotel-single-ci-head">
#                                             <div class="ss-hotel-single-ci-head-right">
#                                                 <div class="ss-hotel-single-cih-content">
#                                                     <div class="d-flex">
#                                                         <span class="ss-hotel-single-cihc-name">حسنین ارکوازی</span>
#                                                         <span class="ss-hotel-single-cih-rate  color-blue"> 4 از 5</span>
#                                                     </div>
#                                                     <span class="ss-hotel-single-cihc-meta color-gray"> 8 آبان 1403</span>
#                                                 </div>
#                                             </div>
#                                                                                             <div class="float-left approved-p">مسافر مورد تایید هتل یار </div>
#                                                                                     </div>
#                                         <div class="ss-hotel-single-ci-body">
#                                             <p>بسیادر تمیز</p>
#                                         </div>
#
#                                         <div class="ss-hotel-single-ci-reviews">
#                                                                                             <div class="ss-hotel-single-cir-good">
#                                                     <div class="ss-hotel-single-cir-item">
#                                                         <i>
#                                                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 352C293.2 352 319.2 334.5 334.4 318.1C343.3 308.4 358.5 307.7 368.3 316.7C378 325.7 378.6 340.9 369.6 350.6C347.7 374.5 309.7 400 256 400C202.3 400 164.3 374.5 142.4 350.6C133.4 340.9 133.1 325.7 143.7 316.7C153.5 307.7 168.7 308.4 177.6 318.1C192.8 334.5 218.8 352 256 352zM208.4 208C208.4 225.7 194 240 176.4 240C158.7 240 144.4 225.7 144.4 208C144.4 190.3 158.7 176 176.4 176C194 176 208.4 190.3 208.4 208zM304.4 208C304.4 190.3 318.7 176 336.4 176C354 176 368.4 190.3 368.4 208C368.4 225.7 354 240 336.4 240C318.7 240 304.4 225.7 304.4 208zM512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 48C141.1 48 48 141.1 48 256C48 370.9 141.1 464 256 464C370.9 464 464 370.9 464 256C464 141.1 370.9 48 256 48z"/></svg>
#                                                         </i>
#                                                         <div class="ss-hotel-single-cir-item-content">
#                                                             <p>تمیزی موقعیت مکانی</p>
#                                                         </div>
#                                                     </div>
#                                                 </div>
#                                                                                                                                         <div class="ss-hotel-single-cir-bad">
#                                                     <div class="ss-hotel-single-cir-item">
#                                                         <i>
#                                                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M143.9 398.6C131.4 394.1 124.9 380.3 129.4 367.9C146.9 319.4 198.9 288 256 288C313.1 288 365.1 319.4 382.6 367.9C387.1 380.3 380.6 394.1 368.1 398.6C355.7 403.1 341.9 396.6 337.4 384.1C328.2 358.5 297.2 336 256 336C214.8 336 183.8 358.5 174.6 384.1C170.1 396.6 156.3 403.1 143.9 398.6V398.6zM208.4 208C208.4 225.7 194 240 176.4 240C158.7 240 144.4 225.7 144.4 208C144.4 190.3 158.7 176 176.4 176C194 176 208.4 190.3 208.4 208zM304.4 208C304.4 190.3 318.7 176 336.4 176C354 176 368.4 190.3 368.4 208C368.4 225.7 354 240 336.4 240C318.7 240 304.4 225.7 304.4 208zM512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 48C141.1 48 48 141.1 48 256C48 370.9 141.1 464 256 464C370.9 464 464 370.9 464 256C464 141.1 370.9 48 256 48z"/></svg>
#                                                         </i>
#                                                         <div class="ss-hotel-single-cir-item-content">
#                                                             <p>ضعف در منوی رستوران</p>
#                                                         </div>
#                                                     </div>
#                                                 </div>
#                                                                                     </div>
#                                     </div>
#
#
#                                                                     <div class="ss-hotel-single-comments-item">
#                                         <div class="ss-hotel-single-ci-head">
#                                             <div class="ss-hotel-single-ci-head-right">
#                                                 <div class="ss-hotel-single-cih-content">
#                                                     <div class="d-flex">
#                                                         <span class="ss-hotel-single-cihc-name">محمدعلی کریمی</span>
#                                                         <span class="ss-hotel-single-cih-rate  color-blue"> 4 از 5</span>
#                                                     </div>
#                                                     <span class="ss-hotel-single-cihc-meta color-gray"> 28 مهر 1403</span>
#                                                 </div>
#                                             </div>
#                                                                                             <div class="float-left approved-p">مسافر مورد تایید هتل یار </div>
#                                                                                     </div>
#                                         <div class="ss-hotel-single-ci-body">
#                                             <p>بعضی از پرسنل پذیرش (احتمالا بابت شلوغی) در انتقال اطلاعات ضعیف بودن و گاهی حس مثبت نداشتیم از تعامل باهاشون.
# در کل افامت خوبی بود و خوش گذشت.</p>
#                                         </div>
#
#                                         <div class="ss-hotel-single-ci-reviews">
#                                                                                             <div class="ss-hotel-single-cir-good">
#                                                     <div class="ss-hotel-single-cir-item">
#                                                         <i>
#                                                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 352C293.2 352 319.2 334.5 334.4 318.1C343.3 308.4 358.5 307.7 368.3 316.7C378 325.7 378.6 340.9 369.6 350.6C347.7 374.5 309.7 400 256 400C202.3 400 164.3 374.5 142.4 350.6C133.4 340.9 133.1 325.7 143.7 316.7C153.5 307.7 168.7 308.4 177.6 318.1C192.8 334.5 218.8 352 256 352zM208.4 208C208.4 225.7 194 240 176.4 240C158.7 240 144.4 225.7 144.4 208C144.4 190.3 158.7 176 176.4 176C194 176 208.4 190.3 208.4 208zM304.4 208C304.4 190.3 318.7 176 336.4 176C354 176 368.4 190.3 368.4 208C368.4 225.7 354 240 336.4 240C318.7 240 304.4 225.7 304.4 208zM512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 48C141.1 48 48 141.1 48 256C48 370.9 141.1 464 256 464C370.9 464 464 370.9 464 256C464 141.1 370.9 48 256 48z"/></svg>
#                                                         </i>
#                                                         <div class="ss-hotel-single-cir-item-content">
#                                                             <p>صبحانه کامل و خوب.<br />
# فضاهای جذاب کافه بام و کافه لابی ششم.</p>
#                                                         </div>
#                                                     </div>
#                                                 </div>
#                                                                                                                                         <div class="ss-hotel-single-cir-bad">
#                                                     <div class="ss-hotel-single-cir-item">
#                                                         <i>
#                                                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M143.9 398.6C131.4 394.1 124.9 380.3 129.4 367.9C146.9 319.4 198.9 288 256 288C313.1 288 365.1 319.4 382.6 367.9C387.1 380.3 380.6 394.1 368.1 398.6C355.7 403.1 341.9 396.6 337.4 384.1C328.2 358.5 297.2 336 256 336C214.8 336 183.8 358.5 174.6 384.1C170.1 396.6 156.3 403.1 143.9 398.6V398.6zM208.4 208C208.4 225.7 194 240 176.4 240C158.7 240 144.4 225.7 144.4 208C144.4 190.3 158.7 176 176.4 176C194 176 208.4 190.3 208.4 208zM304.4 208C304.4 190.3 318.7 176 336.4 176C354 176 368.4 190.3 368.4 208C368.4 225.7 354 240 336.4 240C318.7 240 304.4 225.7 304.4 208zM512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 48C141.1 48 48 141.1 48 256C48 370.9 141.1 464 256 464C370.9 464 464 370.9 464 256C464 141.1 370.9 48 256 48z"/></svg>
#                                                         </i>
#                                                         <div class="ss-hotel-single-cir-item-content">
#                                                             <p>منوی آنلاین کافه ها عموما به روز نشده بود.</p>
#                                                         </div>
#                                                     </div>
#                                                 </div>
#                                                                                     </div>
#                                     </div>
#
#
#                                                                     <div class="ss-hotel-single-comments-item">
#                                         <div class="ss-hotel-single-ci-head">
#                                             <div class="ss-hotel-single-ci-head-right">
#                                                 <div class="ss-hotel-single-cih-content">
#                                                     <div class="d-flex">
#                                                         <span class="ss-hotel-single-cihc-name">علیرضا پیوند</span>
#                                                         <span class="ss-hotel-single-cih-rate  color-blue"> 4 از 5</span>
#                                                     </div>
#                                                     <span class="ss-hotel-single-cihc-meta color-gray"> 24 شهریور 1403</span>
#                                                 </div>
#                                             </div>
#                                                                                             <div class="float-left approved-p">مسافر مورد تایید هتل یار </div>
#                                                                                     </div>
#                                         <div class="ss-hotel-single-ci-body">
#                                             <p>همه چیز بسیار خوب</p>
#                                         </div>
#
#                                         <div class="ss-hotel-single-ci-reviews">
#                                                                                                                                 </div>
#                                     </div>
#
#
#                                                                     <div class="ss-hotel-single-comments-item">
#                                         <div class="ss-hotel-single-ci-head">
#                                             <div class="ss-hotel-single-ci-head-right">
#                                                 <div class="ss-hotel-single-cih-content">
#                                                     <div class="d-flex">
#                                                         <span class="ss-hotel-single-cihc-name">امید اخلاقی</span>
#                                                         <span class="ss-hotel-single-cih-rate  color-blue"> 4 از 5</span>
#                                                     </div>
#                                                     <span class="ss-hotel-single-cihc-meta color-gray"> 17 شهریور 1403</span>
#                                                 </div>
#                                             </div>
#                                                                                             <div class="float-left approved-p">مسافر مورد تایید هتل یار </div>
#                                                                                     </div>
#                                         <div class="ss-hotel-single-ci-body">
#                                             <p>برای بار دوم طی ۵ سال اخیر ، در این هتل اقامت داشتم. جزو ۵ هتل برتر کشور میباشد . شک نکنید و انتخابش کنید . پشیمان نمیشوید.</p>
#                                         </div>
#
#                                         <div class="ss-hotel-single-ci-reviews">
#                                                                                             <div class="ss-hotel-single-cir-good">
#                                                     <div class="ss-hotel-single-cir-item">
#                                                         <i>
#                                                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 352C293.2 352 319.2 334.5 334.4 318.1C343.3 308.4 358.5 307.7 368.3 316.7C378 325.7 378.6 340.9 369.6 350.6C347.7 374.5 309.7 400 256 400C202.3 400 164.3 374.5 142.4 350.6C133.4 340.9 133.1 325.7 143.7 316.7C153.5 307.7 168.7 308.4 177.6 318.1C192.8 334.5 218.8 352 256 352zM208.4 208C208.4 225.7 194 240 176.4 240C158.7 240 144.4 225.7 144.4 208C144.4 190.3 158.7 176 176.4 176C194 176 208.4 190.3 208.4 208zM304.4 208C304.4 190.3 318.7 176 336.4 176C354 176 368.4 190.3 368.4 208C368.4 225.7 354 240 336.4 240C318.7 240 304.4 225.7 304.4 208zM512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 48C141.1 48 48 141.1 48 256C48 370.9 141.1 464 256 464C370.9 464 464 370.9 464 256C464 141.1 370.9 48 256 48z"/></svg>
#                                                         </i>
#                                                         <div class="ss-hotel-single-cir-item-content">
#                                                             <p>پاکیزگی<br />
# محیطی آرام و دلنواز<br />
# کارکنانی خونگرم<br />
# پارکینگهای خوب و مناسب</p>
#                                                         </div>
#                                                     </div>
#                                                 </div>
#                                                                                                                                 </div>
#                                     </div>
#
#
#                                                                     <div class="ss-hotel-single-comments-item">
#                                         <div class="ss-hotel-single-ci-head">
#                                             <div class="ss-hotel-single-ci-head-right">
#                                                 <div class="ss-hotel-single-cih-content">
#                                                     <div class="d-flex">
#                                                         <span class="ss-hotel-single-cihc-name">عظیم غلام پور</span>
#                                                         <span class="ss-hotel-single-cih-rate  color-blue"> 4 از 5</span>
#                                                     </div>
#                                                     <span class="ss-hotel-single-cihc-meta color-gray"> 10 شهریور 1403</span>
#                                                 </div>
#                                             </div>
#                                                                                             <div class="float-left approved-p">مسافر مورد تایید هتل یار </div>
#                                                                                     </div>
#                                         <div class="ss-hotel-single-ci-body">
#                                             <p>بسیارعالی</p>
#                                         </div>
#
#                                         <div class="ss-hotel-single-ci-reviews">
#                                                                                                                                 </div>
#                                     </div>
#
#
#                                                                                     </div>
#
#                     </div>
#                 </div>
#                                     <div class="ss-hotel-single-comments-wrapper btn-load-wrapper">
#                         <div class="btn-load">
#                             <button type="button" class="btn ss-btn ss-btn-blue form-cm-form-btn"  aria-label="Name" onclick="loadComment(this);">
#                                 <span>مشاهده نظرات بیشتر</span>
#                                 <i>
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M449.9 39.96l-48.5 48.53C362.5 53.19 311.4 32 256 32C161.5 32 78.59 92.34 49.58 182.2c-5.438 16.81 3.797 34.88 20.61 40.28c16.97 5.5 34.86-3.812 40.3-20.59C130.9 138.5 189.4 96 256 96c37.96 0 73 14.18 100.2 37.8L311.1 178C295.1 194.8 306.8 223.4 330.4 224h146.9C487.7 223.7 496 215.3 496 204.9V59.04C496 34.99 466.9 22.95 449.9 39.96zM441.8 289.6c-16.94-5.438-34.88 3.812-40.3 20.59C381.1 373.5 322.6 416 256 416c-37.96 0-73-14.18-100.2-37.8L200 334C216.9 317.2 205.2 288.6 181.6 288H34.66C24.32 288.3 16 296.7 16 307.1v145.9c0 24.04 29.07 36.08 46.07 19.07l48.5-48.53C149.5 458.8 200.6 480 255.1 480c94.45 0 177.4-60.34 206.4-150.2C467.9 313 458.6 294.1 441.8 289.6z"/></svg>
#                                 </i>
#                             </button>
#                         </div>
#                     </div>
#                             </div>
#         </section>
#         <!-- Ends: comments -->
#         <!-- Start: form -->
#
#         <!-- Ends: form -->
#         <!-- Start: Review -->
#                 <!-- Ends: review -->
#         <!-- Start: lecture -->
#                     <section id="section-lecture">
#                 <div class="container">
#                     <div class="row">
#                         <div class="col-md-12">
#                             <h3 class="ss-innerpage-head-title">
#                                 <i>
#                                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M224 256c70.7 0 128-57.31 128-128s-57.3-128-128-128C153.3 0 96 57.31 96 128S153.3 256 224 256zM224 32c52.94 0 96 43.06 96 96c0 52.93-43.06 96-96 96S128 180.9 128 128C128 75.06 171.1 32 224 32zM274.7 304H173.3C77.61 304 0 381.6 0 477.3c0 19.14 15.52 34.67 34.66 34.67h378.7C432.5 512 448 496.5 448 477.3C448 381.6 370.4 304 274.7 304zM413.3 480H34.66C33.2 480 32 478.8 32 477.3C32 399.4 95.4 336 173.3 336h101.3C352.6 336 416 399.4 416 477.3C416 478.8 414.8 480 413.3 480z"/></svg>
#                                 </i>قلم مسافران هتل بزرگ شیراز                            </h3>
#                             <div class="ss-hotel-single-comments-wrapper" id="lecture-container">
#                                                                     <div class="ss-hotel-single-comments-item">
#                                         <div class="ss-hotel-single-ci-head">
#                                             <div class="ss-hotel-single-ci-head-right">
#                                                 <div class="ss-hotel-single-cih-content">
#                                                     <span class="ss-hotel-single-cihc-name">نقد و بررسی هتل بزرگ شیراز به قلم مانا</span>
#                                                     <span class="ss-hotel-single-cihc-meta color-gray">نوشته شده در دهم شهریور 1402</span>
#
#                                                 </div>
#                                             </div>
#                                         </div>
#                                         <div class="ss-hotel-single-ci-body">
#
#                                                                                             <div class="ss-hotel-single-dr-ls-item pt-3">
#                                                     <i class="ss-hotel-single-dr-lsi-icon">
#                                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M495 59.6C516.9 81.47 516.9 116.9 495 138.8L182.3 451.6C170.9 462.9 156.9 471.2 141.5 475.8L20.52 511.4C14.9 513 8.827 511.5 4.687 507.3C.5466 503.2-1.002 497.1 .6506 491.5L36.23 370.5C40.76 355.1 49.09 341.1 60.44 329.7L373.2 16.97C395.1-4.897 430.5-4.897 452.4 16.97L495 59.6zM341 94.4L417.6 170.1L472.4 116.2C481.8 106.8 481.8 91.6 472.4 82.23L429.8 39.6C420.4 30.23 405.2 30.23 395.8 39.6L341 94.4zM318.4 117L83.07 352.4C75.5 359.9 69.95 369.3 66.93 379.6L39.63 472.4L132.4 445.1C142.7 442.1 152.1 436.5 159.6 428.9L394.1 193.6L318.4 117z"/></svg>
#                                                     </i>
#                                                     <span class="ss-hotel-single-dr-lsi-sub">مشخصات کلی (ابعاد، امکانات، جغرافیایی)</span>
#
#                                                 </div>
#                                                 <div>
#                                                     <p class="ss-single-comments-clib-txt text-justify">
#                                                          به محض ورود به شیراز در مکانی بسیار مناسب بدون هیچ زحمتی هتل قابل رویت است.                                                    </p>
#                                                 </div>
#                                                                                             <div class="ss-hotel-single-dr-ls-item pt-3">
#                                                     <i class="ss-hotel-single-dr-lsi-icon">
#                                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M495 59.6C516.9 81.47 516.9 116.9 495 138.8L182.3 451.6C170.9 462.9 156.9 471.2 141.5 475.8L20.52 511.4C14.9 513 8.827 511.5 4.687 507.3C.5466 503.2-1.002 497.1 .6506 491.5L36.23 370.5C40.76 355.1 49.09 341.1 60.44 329.7L373.2 16.97C395.1-4.897 430.5-4.897 452.4 16.97L495 59.6zM341 94.4L417.6 170.1L472.4 116.2C481.8 106.8 481.8 91.6 472.4 82.23L429.8 39.6C420.4 30.23 405.2 30.23 395.8 39.6L341 94.4zM318.4 117L83.07 352.4C75.5 359.9 69.95 369.3 66.93 379.6L39.63 472.4L132.4 445.1C142.7 442.1 152.1 436.5 159.6 428.9L394.1 193.6L318.4 117z"/></svg>
#                                                     </i>
#                                                     <span class="ss-hotel-single-dr-lsi-sub">ویژگی هتل بزرگ شیراز</span>
#
#                                                 </div>
#                                                 <div>
#                                                     <p class="ss-single-comments-clib-txt text-justify">
#                                                          پذیرش هتل و نحوه چیدمان نشان میداد که هنوز بعضی از کارهای تجهیز هتل باقیست .از نحوه لباس پوشیدن و آرایش پرسنل هتل تلاش آنها را در مرتب بودن می شد فهمید. پذیرایی با عرقیات معروف شیراز و خوشامدگویی ...طراحی هتل خوب به نظر می رسید لابی کوچکی داشت که آرامش حضور مهمانان یا رفت و امدهایی که مرتبط با مسافران نبود آزاردهنده بود.و متاسفانه حس کنجکاوی با نگاه پرسنل که از استانداردهای هتل 5 ستاره خارج است.
# نقص در وسایل تجهیز هتل برای 2 نفر به طور مثال قراردادن یک جفت روفرشی حوله ای در یک اتاق 2 نفره و یا عدم پیش بینی هتل تن پوش سایز بزرگ که خوشبختانه در اولین تماس مرتفع شد.
# هزینه بسیار بالا جهت به راه انداختن چنین مکانی قابل تحسین است ولی مدیریت نیروی انسانی از جمله رهبری رفتار کارکنان مخصوصا در رستورانها جای بازبینی دارد.همچنین در بحث نگهداری تجهیزات نیاز به دقت بیشتر دارند.                                                    </p>
#                                                 </div>
#                                                                                             <div class="ss-hotel-single-dr-ls-item pt-3">
#                                                     <i class="ss-hotel-single-dr-lsi-icon">
#                                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M495 59.6C516.9 81.47 516.9 116.9 495 138.8L182.3 451.6C170.9 462.9 156.9 471.2 141.5 475.8L20.52 511.4C14.9 513 8.827 511.5 4.687 507.3C.5466 503.2-1.002 497.1 .6506 491.5L36.23 370.5C40.76 355.1 49.09 341.1 60.44 329.7L373.2 16.97C395.1-4.897 430.5-4.897 452.4 16.97L495 59.6zM341 94.4L417.6 170.1L472.4 116.2C481.8 106.8 481.8 91.6 472.4 82.23L429.8 39.6C420.4 30.23 405.2 30.23 395.8 39.6L341 94.4zM318.4 117L83.07 352.4C75.5 359.9 69.95 369.3 66.93 379.6L39.63 472.4L132.4 445.1C142.7 442.1 152.1 436.5 159.6 428.9L394.1 193.6L318.4 117z"/></svg>
#                                                     </i>
#                                                     <span class="ss-hotel-single-dr-lsi-sub">اطراف هتل (تفریح و سرگرمی ، رستورانها ، مناطق دیدنی)</span>
#
#                                                 </div>
#                                                 <div>
#                                                     <p class="ss-single-comments-clib-txt text-justify">
#                                                          بهترین رستورانها ,حافظیه ,مرکز تفریحی ... در نزدیکترین فاصله به هتل قراردارند                                                    </p>
#                                                 </div>
#                                                                                             <div class="ss-hotel-single-dr-ls-item pt-3">
#                                                     <i class="ss-hotel-single-dr-lsi-icon">
#                                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M495 59.6C516.9 81.47 516.9 116.9 495 138.8L182.3 451.6C170.9 462.9 156.9 471.2 141.5 475.8L20.52 511.4C14.9 513 8.827 511.5 4.687 507.3C.5466 503.2-1.002 497.1 .6506 491.5L36.23 370.5C40.76 355.1 49.09 341.1 60.44 329.7L373.2 16.97C395.1-4.897 430.5-4.897 452.4 16.97L495 59.6zM341 94.4L417.6 170.1L472.4 116.2C481.8 106.8 481.8 91.6 472.4 82.23L429.8 39.6C420.4 30.23 405.2 30.23 395.8 39.6L341 94.4zM318.4 117L83.07 352.4C75.5 359.9 69.95 369.3 66.93 379.6L39.63 472.4L132.4 445.1C142.7 442.1 152.1 436.5 159.6 428.9L394.1 193.6L318.4 117z"/></svg>
#                                                     </i>
#                                                     <span class="ss-hotel-single-dr-lsi-sub">هتل بزرگ شیراز را به چه کسانی پیشنهاد می کنید</span>
#
#                                                 </div>
#                                                 <div>
#                                                     <p class="ss-single-comments-clib-txt text-justify">
#                                                         هنوز به امکانات هتل به طور کامل با توجه به تبلیغاتشون آماده نیست مخصوصا مرکز خرید پس اگه از هتل خودتون انتظار این چنین دارید کمی صبر کنید .                                                    </p>
#                                                 </div>
#                                                                                             <div class="ss-hotel-single-dr-ls-item pt-3">
#                                                     <i class="ss-hotel-single-dr-lsi-icon">
#                                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M495 59.6C516.9 81.47 516.9 116.9 495 138.8L182.3 451.6C170.9 462.9 156.9 471.2 141.5 475.8L20.52 511.4C14.9 513 8.827 511.5 4.687 507.3C.5466 503.2-1.002 497.1 .6506 491.5L36.23 370.5C40.76 355.1 49.09 341.1 60.44 329.7L373.2 16.97C395.1-4.897 430.5-4.897 452.4 16.97L495 59.6zM341 94.4L417.6 170.1L472.4 116.2C481.8 106.8 481.8 91.6 472.4 82.23L429.8 39.6C420.4 30.23 405.2 30.23 395.8 39.6L341 94.4zM318.4 117L83.07 352.4C75.5 359.9 69.95 369.3 66.93 379.6L39.63 472.4L132.4 445.1C142.7 442.1 152.1 436.5 159.6 428.9L394.1 193.6L318.4 117z"/></svg>
#                                                     </i>
#                                                     <span class="ss-hotel-single-dr-lsi-sub">چه زمانی به این هتل سفر کنیم</span>
#
#                                                 </div>
#                                                 <div>
#                                                     <p class="ss-single-comments-clib-txt text-justify">
#                                                          بهترین فصل سفر به شیراز بهار و یا پاییز است که با توجه به نزدیکی باغات و حافظیه به هتل تصویر بسار زیبایی از شهر شیراز از پنجره های این هتل در انتظاز شماست.                                                    </p>
#                                                 </div>
#                                                                                             <div class="ss-hotel-single-dr-ls-item pt-3">
#                                                     <i class="ss-hotel-single-dr-lsi-icon">
#                                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M495 59.6C516.9 81.47 516.9 116.9 495 138.8L182.3 451.6C170.9 462.9 156.9 471.2 141.5 475.8L20.52 511.4C14.9 513 8.827 511.5 4.687 507.3C.5466 503.2-1.002 497.1 .6506 491.5L36.23 370.5C40.76 355.1 49.09 341.1 60.44 329.7L373.2 16.97C395.1-4.897 430.5-4.897 452.4 16.97L495 59.6zM341 94.4L417.6 170.1L472.4 116.2C481.8 106.8 481.8 91.6 472.4 82.23L429.8 39.6C420.4 30.23 405.2 30.23 395.8 39.6L341 94.4zM318.4 117L83.07 352.4C75.5 359.9 69.95 369.3 66.93 379.6L39.63 472.4L132.4 445.1C142.7 442.1 152.1 436.5 159.6 428.9L394.1 193.6L318.4 117z"/></svg>
#                                                     </i>
#                                                     <span class="ss-hotel-single-dr-lsi-sub">تناسب قیمت با کیفیت و امکانات هتل بزرگ شیراز</span>
#
#                                                 </div>
#                                                 <div>
#                                                     <p class="ss-single-comments-clib-txt text-justify">
#                                                          متناسب و معقول                                                    </p>
#                                                 </div>
#                                                                                             <div class="ss-hotel-single-dr-ls-item pt-3">
#                                                     <i class="ss-hotel-single-dr-lsi-icon">
#                                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M495 59.6C516.9 81.47 516.9 116.9 495 138.8L182.3 451.6C170.9 462.9 156.9 471.2 141.5 475.8L20.52 511.4C14.9 513 8.827 511.5 4.687 507.3C.5466 503.2-1.002 497.1 .6506 491.5L36.23 370.5C40.76 355.1 49.09 341.1 60.44 329.7L373.2 16.97C395.1-4.897 430.5-4.897 452.4 16.97L495 59.6zM341 94.4L417.6 170.1L472.4 116.2C481.8 106.8 481.8 91.6 472.4 82.23L429.8 39.6C420.4 30.23 405.2 30.23 395.8 39.6L341 94.4zM318.4 117L83.07 352.4C75.5 359.9 69.95 369.3 66.93 379.6L39.63 472.4L132.4 445.1C142.7 442.1 152.1 436.5 159.6 428.9L394.1 193.6L318.4 117z"/></svg>
#                                                     </i>
#                                                     <span class="ss-hotel-single-dr-lsi-sub">چگونه حداقل قیمت را پرداخت نماییم</span>
#
#                                                 </div>
#                                                 <div>
#                                                     <p class="ss-single-comments-clib-txt text-justify">
#                                                          یار من گشت به شیراز هتل یار          بی تو هیچ کجا نروم نه به دیاری دبدار
# به یاری تو در کام سخت و عذاب جان       تو باش یارم همه وقت و همه جا هتل یار                                                    </p>
#                                                 </div>
#                                                                                             <div class="ss-hotel-single-dr-ls-item pt-3">
#                                                     <i class="ss-hotel-single-dr-lsi-icon">
#                                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M495 59.6C516.9 81.47 516.9 116.9 495 138.8L182.3 451.6C170.9 462.9 156.9 471.2 141.5 475.8L20.52 511.4C14.9 513 8.827 511.5 4.687 507.3C.5466 503.2-1.002 497.1 .6506 491.5L36.23 370.5C40.76 355.1 49.09 341.1 60.44 329.7L373.2 16.97C395.1-4.897 430.5-4.897 452.4 16.97L495 59.6zM341 94.4L417.6 170.1L472.4 116.2C481.8 106.8 481.8 91.6 472.4 82.23L429.8 39.6C420.4 30.23 405.2 30.23 395.8 39.6L341 94.4zM318.4 117L83.07 352.4C75.5 359.9 69.95 369.3 66.93 379.6L39.63 472.4L132.4 445.1C142.7 442.1 152.1 436.5 159.6 428.9L394.1 193.6L318.4 117z"/></svg>
#                                                     </i>
#                                                     <span class="ss-hotel-single-dr-lsi-sub">سایر موارد</span>
#
#                                                 </div>
#                                                 <div>
#                                                     <p class="ss-single-comments-clib-txt text-justify">
#                                                         بهترین قیمتها را تا به اکنون از طریق سایت هتل یار تونستم بدست بیارم .                                                     </p>
#                                                 </div>
#
#                                         </div>
#                                     </div>
#
#                             </div>
#
#                         </div>
#                     </div>
#                                             <input type="hidden" name="hotelCode" value="726">
#                         <div class="ss-hotel-single-comments-wrapper btn-load-wrapper">
#                             <div class="row">
#                                 <div class="btn-load">
#                                     <button type="button" class="btn ss-btn ss-btn-blue form-cm-form-btn"  aria-label="Name" onclick="loadLecture(this);">
#                                         <span>نمایش بیشتر</span>
#                                         <i>
#                                             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path>
#                                             </svg>
#                                         </i>
#                                     </button>
#                                 </div>
#                             </div>
#                         </div>
#                                     </div>
#             </section>
#                 <!-- Ends: lecture -->
#         <!-- Start: suggestion -->
#                     <section class="ss-single-hotel-suggestion">
#                 <div class="container">
#                     <div class="row">
#                         <div class="col-md-12">
#                             <h3 class="ss-innerpage-head-title more-link">
#                                 <div class="ss-innerpage-head-title-right">
#                                     <i>
#                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M176 96C184.8 96 192 103.2 192 112V144C192 152.8 184.8 160 176 160H144C135.2 160 128 152.8 128 144V112C128 103.2 135.2 96 144 96H176zM224 112C224 103.2 231.2 96 240 96H272C280.8 96 288 103.2 288 112V144C288 152.8 280.8 160 272 160H240C231.2 160 224 152.8 224 144V112zM368 96C376.8 96 384 103.2 384 112V144C384 152.8 376.8 160 368 160H336C327.2 160 320 152.8 320 144V112C320 103.2 327.2 96 336 96H368zM128 208C128 199.2 135.2 192 144 192H176C184.8 192 192 199.2 192 208V240C192 248.8 184.8 256 176 256H144C135.2 256 128 248.8 128 240V208zM272 192C280.8 192 288 199.2 288 208V240C288 248.8 280.8 256 272 256H240C231.2 256 224 248.8 224 240V208C224 199.2 231.2 192 240 192H272zM320 208C320 199.2 327.2 192 336 192H368C376.8 192 384 199.2 384 208V240C384 248.8 376.8 256 368 256H336C327.2 256 320 248.8 320 240V208zM488 0C501.3 0 512 10.75 512 24C512 37.25 501.3 48 488 48H480V464H488C501.3 464 512 474.7 512 488C512 501.3 501.3 512 488 512H24C10.75 512 0 501.3 0 488C0 474.7 10.75 464 24 464H32V48H24C10.75 48 0 37.25 0 24C0 10.75 10.75 0 24 0H488zM80 48V464H208V384H176C167.2 384 159.9 376.8 161.3 368.1C168.9 322.6 208.4 288 256 288C303.6 288 343.1 322.6 350.7 368.1C352.1 376.8 344.8 384 336 384H304V464H432V48H80z"/></svg>
#                                     </i>هتل های مشابه
#                                 </div>
#                             </h3>
#                             <div class="main-hsu-list owl-carousel owl-theme">
#                                                                     <a href="https://hotelyar.com/hotel/47/هتل-پرسپولیس-شیراز?checkin=1403-11-14&checkout=1403-11-15" class="hotel-thumb hsu-item item-hover">
#                                         <span class="text-off">text off</span>
#                                                                                                                                     <div class="hotel-thumb-off">
#                                                     <span class="hotel-thumb-off-title">تخفیف</span>
#                                                     <span class="hotel-thumb-off-number ">16<span>%</span></span>
#                                                 </div>
#                                                                                     <img class="owl-lazy" data-src="https://hotelyar.com/pic/47small.jpg" alt="عکس هتل پرسپولیس شیراز">
#                                         <div class="hotel-thumb-content">
#                                             <h2 class="hotel-thumb-title">هتل پرسپولیس شیراز</h2>
#                                             <div class="stars-wrapper stars-small hotel-thumb-stars">
#                                                 <div aria-hidden="true" focusable="false" class="stars"><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span></div>
#                     <span class="stars-title color-gray">(پنج ستاره)</span>                                            </div>
#                                                                                             <div class="hotel-thumb-price">
#                                                     <span class="color-red hotel-thumb-price-num">1,900,000</span>
#                                                     <span class="color-red hotel-thumb-price-name">تومان</span>
#                                                 </div>
#                                                                                     </div>
#                                     </a>
#                                                                     <a href="https://hotelyar.com/hotel/1082/هتل-زندیه-شیراز?checkin=1403-11-14&checkout=1403-11-15" class="hotel-thumb hsu-item item-hover">
#                                         <span class="text-off">text off</span>
#                                                                                                                                     <div class="hotel-thumb-off">
#                                                     <span class="hotel-thumb-off-title">تخفیف</span>
#                                                     <span class="hotel-thumb-off-number ">14<span>%</span></span>
#                                                 </div>
#                                                                                     <img class="owl-lazy" data-src="https://hotelyar.com/pic/1082small.jpg" alt="عکس هتل زندیه شیراز">
#                                         <div class="hotel-thumb-content">
#                                             <h2 class="hotel-thumb-title">هتل زندیه شیراز</h2>
#                                             <div class="stars-wrapper stars-small hotel-thumb-stars">
#                                                 <div aria-hidden="true" focusable="false" class="stars"><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span></div>
#                     <span class="stars-title color-gray">(پنج ستاره)</span>                                            </div>
#                                                                                             <div class="hotel-thumb-price">
#                                                     <span class="color-red hotel-thumb-price-num">3,180,000</span>
#                                                     <span class="color-red hotel-thumb-price-name">تومان</span>
#                                                 </div>
#                                                                                     </div>
#                                     </a>
#                                                                     <a href="https://hotelyar.com/hotel/228/هتل-هما-شیراز?checkin=1403-11-14&checkout=1403-11-15" class="hotel-thumb hsu-item item-hover">
#                                         <span class="text-off">text off</span>
#                                                                                                                             <img class="owl-lazy" data-src="https://hotelyar.com/pic/228small.jpg" alt="عکس هتل هما شیراز">
#                                         <div class="hotel-thumb-content">
#                                             <h2 class="hotel-thumb-title">هتل هما شیراز</h2>
#                                             <div class="stars-wrapper stars-small hotel-thumb-stars">
#                                                 <div aria-hidden="true" focusable="false" class="stars"><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span></div>
#                     <span class="stars-title color-gray">(پنج ستاره)</span>                                            </div>
#                                                                                             <div class="hotel-thumb-price">
#                                                     <span class="color-red hotel-thumb-price-num">2,530,000</span>
#                                                     <span class="color-red hotel-thumb-price-name">تومان</span>
#                                                 </div>
#                                                                                     </div>
#                                     </a>
#                                                                     <a href="https://hotelyar.com/hotel/229/هتل-پارس-شیراز?checkin=1403-11-14&checkout=1403-11-15" class="hotel-thumb hsu-item item-hover">
#                                         <span class="text-off">text off</span>
#                                                                                                                                     <div class="hotel-thumb-off">
#                                                     <span class="hotel-thumb-off-title">تخفیف</span>
#                                                     <span class="hotel-thumb-off-number ">13<span>%</span></span>
#                                                 </div>
#                                                                                     <img class="owl-lazy" data-src="https://hotelyar.com/pic/229small.jpg" alt="عکس هتل پارس شیراز">
#                                         <div class="hotel-thumb-content">
#                                             <h2 class="hotel-thumb-title">هتل پارس شیراز</h2>
#                                             <div class="stars-wrapper stars-small hotel-thumb-stars">
#                                                 <div aria-hidden="true" focusable="false" class="stars"><span class="star stars-empty-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span></div>
#                     <span class="stars-title color-gray">(چهار ستاره)</span>                                            </div>
#                                                                                             <div class="hotel-thumb-price">
#                                                     <span class="color-red hotel-thumb-price-num">1,497,000</span>
#                                                     <span class="color-red hotel-thumb-price-name">تومان</span>
#                                                 </div>
#                                                                                     </div>
#                                     </a>
#                                                                     <a href="https://hotelyar.com/hotel/1070/هتل-رویال-شیراز?checkin=1403-11-14&checkout=1403-11-15" class="hotel-thumb hsu-item item-hover">
#                                         <span class="text-off">text off</span>
#                                                                                 <img class="owl-lazy" data-src="https://hotelyar.com/pic/1070small.jpg" alt="عکس هتل رویال شیراز">
#                                         <div class="hotel-thumb-content">
#                                             <h2 class="hotel-thumb-title">هتل رویال شیراز</h2>
#                                             <div class="stars-wrapper stars-small hotel-thumb-stars">
#                                                 <div aria-hidden="true" focusable="false" class="stars"><span class="star stars-empty-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span><span class="star stars-full-star" ></span></div>
#                     <span class="stars-title color-gray">(چهار ستاره)</span>                                            </div>
#                                                                                     </div>
#                                     </a>
#                                                             </div>
#                         </div>
#                     </div>
#                 </div>
#             </section>
#                 <!-- Ends: suggestion -->
#         <!-- Start: faq -->
#         <section class="ss-innerpage-faq-section">
#                     </section>
#         <!-- Ends: faq -->
#         <section class="ss-single-hotel-suggestion">
#             <div class="container">
#                 <div class="row">
#                     <div class="col-md-12">
#                         <button type="button" class="ss-btn special-offer-la-item item-hover" onclick="goBook();" style="background: url('/static/img/dummy/home-sp-ad-02.jpg') no-repeat bottom left #ffdbbd;">
#                             <span class="special-offer-lai-more btn ss-btn ss-btn-red ss-btn-small ">رزرو هتل بزرگ شیراز                            </span>
#                         </button>
#                     </div>
#                 </div>
#             </div>
#         </section>
#         <!-- Ends: features -->
#             <footer>
#         <div class="container">
#             <div class="row">
#                 <div class="col-md-12">
#                     <div class="footer-main">
#                         <div class="footer-links">
#                             <h4 class="footer-links-title">اطلاعات هتل ها در شهرهای ایران</h4>
#                             <ul class="footer-links-list">
#                                 <li><span>تهران »</span> <a href="https://hotelyar.com/city/11/هتلهای-تهران">هتل های
#                                         تهران</a></li>
#                                 <li><span>مشهد »</span> <a href="https://hotelyar.com/city/27/هتلهای-مشهد">هتل های
#                                         مشهد</a></li>
#                                 <li><span>اصفهان »</span> <a href="https://hotelyar.com/city/4/هتلهای-اصفهان">هتل های
#                                         اصفهان</a></li>
#                                 <li><span>شیراز »</span> <a href="https://hotelyar.com/city/20/هتلهای-شیراز">هتل های
#                                         شیراز</a></li>
#                                 <li><span>تبریز »</span> <a href="https://hotelyar.com/city/10/هتلهای-تبریز">هتل های
#                                         تبریز</a></li>
#                                 <li><span>یزد »</span> <a href="https://hotelyar.com/city/29/هتلهای-یزد">هتل های
#                                         یزد</a></li>
#                                 <li><span>کیش »</span> <a href="https://hotelyar.com/city/23/هتلهای-کیش">هتل های
#                                         کیش</a></li>
#                                 <li><span>رشت »</span> <a href="https://hotelyar.com/city/112/هتلهای-رشت">هتل های
#                                         رشت</a></li>
#                                 <li><a href="https://hotelyar.com/لیست-هتل-های-ایران"> رزرو هتل در سایر شهرهای
#                                         ایران</a></li>
#                                 <li><a href="https://hotelyar.com/هتلهای-ایران-روی-نقشه"> نمایش هتل ها روی نقشه
#                                         ایران</a></li>
#                                 <li><a href="https://hotelyar.com/مقایسه-هتل-ها">مقایسه هتل ها</a></li>
#                             </ul>
#                         </div>
#                         <div class="footer-badges">
#                             <div class="footer-badges-list">
#                                 <div class="footer-badges-item" id="samandehi">
#                                     <img id='jxlzesgtesgtjxlznbqeapfujzpe' style='cursor:pointer;width: 100%;' onclick='window.open("https://logo.samandehi.ir/Verify.aspx?id=1001257&p=rfthobpdobpdrfthuiwkdshwjyoe", "Popup","toolbar=no, scrollbars=no, location=no, statusbar=no, menubar=no, resizable=0, width=450, height=630, top=30")' alt='logo-samandehi' src='https://logo.samandehi.ir/logo.aspx?id=1001257&p=nbpdlymalymanbpdodrfujynyndt'/>
#                                 </div>
#                                 <div class="footer-badges-item loaded" id="enamad">
#                                     <a referrerpolicy="origin" target="_blank" href="https://trustseal.enamad.ir/?id=38389&Code=UAnfdasFlKaH5XnRw9nMebYPPBiUpouT"><img referrerpolicy="origin" class="lazyload" src="https://trustseal.enamad.ir/logo.aspx?id=38389&Code=UAnfdasFlKaH5XnRw9nMebYPPBiUpouT" width="120" height="120" alt="Enamad" style="cursor:pointer" id="UAnfdasFlKaH5XnRw9nMebYPPBiUpouT"></a>
#                                 </div>
#                             </div>
#                         </div>
#                     </div>
#                     <div class="footer-about">
#                         <div class="footer-about-text">
#                             <a class="footer-at-logo" href="https://hotelyar.com" aria-label="هتل یار"><img src="https://hotelyar.com/static/img/theme/logo-footer.svg" alt="هتل یار"></a>
#                             <p>هتل یار (شبکه رزرواسیون اینترنتی هتل های ایران) اولین و بزرگترین شبکه رزرو هتل های ایران
#                                 است که از سال 1384 امکان رزرو هتل در بیش از 1500 هتل و هتل آپارتمان را برای مسافران فراهم
#                                 می کند. با انجام نظرسنجی های مداوم همواره تلاش می شود تنها هتل هایی که رضایت مسافرین را
#                                 جلب نموده اند در لیست هتل ها و هتل آپارتمان های سایت قرار داشته باشند که شامل همه
#                                 مسیرهای پرسفر داخلی از جمله مشهد(هتل های مشهد)، تهران، شیراز، اصفهان، کیش(هتل های کیش)،
#                                 مازندران، گیلان، تبریز، اهواز، کردستان، کلاردشت و بسیاری از هتل آپارتمان های قابل قبول
#                                 در سراسر کشور می شود. نقشه راه، راهنمای سفر و گزارش آب و هوا برای اغلب مسیرها نیز قابل
#                                 مشاهده است</p>
#                         </div>
#                         <div class="footer-about-newsletter">
#                             <h4 class="footer-an-title">عضویت در خبرنامه رزرو هتل</h4>
#                             <form class="footer-an-form" id="frmSubscribe">
#                                 <input class="form-control input subscribeEmailInput" type="text" name="subscribeEmail"
#                                        placeholder="ایمیل خود را وارد نمایید">
#                                 <button type="button" aria-label="Name" onclick="emailSubscribe(this);">
#                                     <i>
#                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
#                                             <path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path>
#                                         </svg>
#                                     </i>
#                                 </button>
#                             </form>
#                             <h4 class="footer-an-title">هتل یار در شبکه های اجتماعی</h4>
#                             <div class="footer-an-social">
#                                 <a href="https://twitter.com/home?status=https://hotelyar.com/hotel/726/%D9%87%D8%AA%D9%84-%D8%A8%D8%B2%D8%B1%DA%AF-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2" target="_blank" aria-label="اشتراک گزاری هتل یار در توییتر" rel="nofollow">
#                                     <i>
#                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
#                                             <path d="M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z"/>
#                                         </svg>
#                                     </i>
#                                 </a>
#                                 <a href="http://t.me/share/?url=https://hotelyar.com/hotel/726/%D9%87%D8%AA%D9%84-%D8%A8%D8%B2%D8%B1%DA%AF-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2" target="_blank" aria-label="اشتراک گزاری هتل یار در تلگرام" rel="nofollow">
#                                     <i>
#                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512">
#                                             <path d="M248,8C111.033,8,0,119.033,0,256S111.033,504,248,504,496,392.967,496,256,384.967,8,248,8ZM362.952,176.66c-3.732,39.215-19.881,134.378-28.1,178.3-3.476,18.584-10.322,24.816-16.948,25.425-14.4,1.326-25.338-9.517-39.287-18.661-21.827-14.308-34.158-23.215-55.346-37.177-24.485-16.135-8.612-25,5.342-39.5,3.652-3.793,67.107-61.51,68.335-66.746.153-.655.3-3.1-1.154-4.384s-3.59-.849-5.135-.5q-3.283.746-104.608,69.142-14.845,10.194-26.894,9.934c-8.855-.191-25.888-5.006-38.551-9.123-15.531-5.048-27.875-7.717-26.8-16.291q.84-6.7,18.45-13.7,108.446-47.248,144.628-62.3c68.872-28.647,83.183-33.623,92.511-33.789,2.052-.034,6.639.474,9.61,2.885a10.452,10.452,0,0,1,3.53,6.716A43.765,43.765,0,0,1,362.952,176.66Z"/>
#                                         </svg>
#                                     </i>
#                                 </a>
#                                 <a href="http://www.facebook.com/sharer.php?u=https://hotelyar.com/hotel/726/%D9%87%D8%AA%D9%84-%D8%A8%D8%B2%D8%B1%DA%AF-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2" target="_blank" aria-label="اشتراک گزاری هتل یار در فیسبوک" rel="nofollow">
#                                     <i>
#                                         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
#                                             <path d="M504 256C504 119 393 8 256 8S8 119 8 256c0 123.78 90.69 226.38 209.25 245V327.69h-63V256h63v-54.64c0-62.15 37-96.48 93.67-96.48 27.14 0 55.52 4.84 55.52 4.84v61h-31.28c-30.8 0-40.41 19.12-40.41 38.73V256h68.78l-11 71.69h-57.78V501C413.31 482.38 504 379.78 504 256z"/>
#                                         </svg>
#                                     </i>
#                                 </a>
#                             </div>
#                         </div>
#                     </div>
#                     <div class="footer-copyright">
#                         <p>هتل یار، رزرو هتل و هتل آپارتمان در همه شهرهای ایران؛ هتل های مشهد، کیش، تهران، اصفهان، شیراز
#                             و ... برای سفرهای تفریحی، کاری، توریستی و زیارتی</p>
#                         <small>© کلیه حقوق مادی و معنوی وبسایت هتل یار متعلق به شرکت آرنیکا مهر کیش می باشد</small>
#                         <ul class="footer-copyright-links">
#                             <li><a href="https://hotelyar.com/اطلس-راه-های-کشور">راهنمای جامع راه ها</a></li>
#                             <li><a href="https://hotelyar.com/مسیر-های-پرطرفدار">مسیر های پرطرفدار</a></li>
#                             <li><a href="https://hotelyar.com/توصیه-های-سفر">توصیه های سفر</a></li>
#                             <li><a href="https://hotelyar.com/نقشه-محورهای-راه-آهن">نقشه محورهای راه آهن</a></li>
#                             <li><a href="https://hotelyar.com/نقشه-فرودگاه-مهرآباد">نقشه فرودگاه مهرآباد</a></li>
#                             <li><a href="https://hotelyar.com/راهنما">راهنما</a></li>
#                             <li><a href="https://hotelyar.com/تماس-با-هتلیار">تماس با ما</a></li>
#                             <li><a href="https://hotelyar.com/تماس-با-هتلیار">ارائه پیشنهاد</a></li>
#                             <li><a href="https://hotelyar.com/privacy.php">Privacy policy</a></li>
#                         </ul>
#                     </div>
#                 </div>
#             </div>
#         </div>
#     </footer>
#         </div>
#             <script type="application/ld+json">
#
#         {
#             "@context": "http://schema.org",
#             "@type": "Hotel",
#             "name": "هتل بزرگ شیراز",
#             "url" : "http:https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز",
#             "image": "https://hotelyar.com/pic/726small.jpg",
#             "description": "رزرو هتل بزرگ شیراز در سایت هتل یار، مقایسه لیست قیمت اتاق ها و امکان کنسلی رایگان، آدرس و تلفن هتل + تضمین قیمت و نظرات کاربران | هتل یار",
#                     "aggregateRating": {
#                 "@type": "AggregateRating",
#                 "ratingValue": "4.4",
#                 "reviewCount": "55"
#             },
#                     "address":{
#             "@type" : "PostalAddress",
#             "streetAddress": "شیراز - دروازه قرآن - هتل بزرگ شیراز",
#                 "addressLocality": "شیراز - دروازه قرآن - هتل بزرگ شیراز",
#                 "addressRegion": "شیراز",
#                 "addressCountry": "ایران"
#             },
#             "telephone": "+982144698615",
#             "numberOfRooms": "158",
#             "checkinTime": "",
#             "checkoutTime": "",
#             "hasMap":"https://maps.google.com/maps?q=29.634857,52.560072",
#             "geo" : {"@type" : "GeoCoordinates", "latitude" : "29.634857", "longitude" : "52.560072"},
#                     "priceRange": "شروع قیمت از 3,376,000",
#                      "starRating": {
#             "@type" : "http://schema.org/Rating",
#             "ratingValue": "5"
#             },
#             "result":{
#                 "@type":"LodgingReservation",
#                 "name":"رزرو هتل"
#             },
#             "containedInPlace":{
#                 "@type":"Place",
#                 "name": "هتل بزرگ شیراز",
#                 "url" : "http:https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز",
#                 "hasMap":"https://maps.google.com/maps?q=29.634857,52.560072",
#                 "address":{
#                     "@type" : "PostalAddress",
#                     "streetAddress": "شیراز - دروازه قرآن - هتل بزرگ شیراز",
#                     "addressLocality": "شیراز - دروازه قرآن - هتل بزرگ شیراز",
#                     "addressRegion": "شیراز",
#                     "addressCountry": "ایران"
#                 }
#             },
#
#             "bed": [
#                             { "@type" : "BedDetails", "name" : "اتاق دو تخته برای یکنفر", "numberOfBeds" : "1" },
#                                         { "@type" : "BedDetails", "name" : "اتاق دو تخته", "numberOfBeds" : "2" },
#                                         { "@type" : "BedDetails", "name" : "اتاق دو تخته", "numberOfBeds" : "2" },
#                                         { "@type" : "BedDetails", "name" : "سوئیت کانکت", "numberOfBeds" : "4" },
#                             ],
# "occupancy": {
#     "@type" : "QuantitativeValue",
#     "maxValue" : "2"
# },
# "amenityFeature": [
#                         {"@type" : "LocationFeatureSpecification", "value": "True", "name": "تلویزیون"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "استخر"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "سوئیت"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "رستوران"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "اینترنت"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "سرویس فرنگی"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "سرویس ایرانی"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "پارکینگ"},
#                             {"@type" : "LocationFeatureSpecification", "value": "False", "name": "ترانسفر فرودگاهی "},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "نمازخانه"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "لابی"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "ماهواره"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "سالن ورزش"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "فروشگاه و غرفه"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "کافی شاپ"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "اینترنت در لابی"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "بیلیارد"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "تلفن در اتاق"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "سونا و جکوزی"},
#                             {"@type" : "LocationFeatureSpecification", "value": "True", "name": "یخچال"},
#                     ]
#     }
#     </script>
#     <!-- Ends: json schema -->
#     <!-- Ends: Main Wrapper -->
#         <script type="text/javascript" src="https://hotelyar.com/static/js/jquery-migrate.min.js"></script>
#
#         <script src="https://hotelyar.com/static/js/plugin.js?v=7"></script>
#     <script src="https://hotelyar.com/static/js/fa.js?v=21"></script>
#         <script src="https://hotelyar.com/static/plugin/OwlCarousel2-2.3.4/owl.carousel.min.js"></script>
#             <script src="https://hotelyar.com/static/plugin/datepicker/js/datepicker.js?version=4"></script>
#         <script src="https://hotelyar.com/static/plugin/offcanvasmenu/off-convas-menu.js"></script>
#
#         <script src="https://hotelyar.com/static/plugin/lazyload/jquery.lazy.min.js"></script>
#
#
#     <script src="https://hotelyar.com/static/js/custom.js?rnd=163"></script>
#     <script>
#         (function (i, s, o, g, r, a, m) {
#             i['GoogleAnalyticsObject'] = r;
#             i[r] = i[r] || function () {
#                 (i[r].q = i[r].q || []).push(arguments)
#             }, i[r].l = 1 * new Date();
#             a = s.createElement(o),
#                 m = s.getElementsByTagName(o)[0];
#             a.async = 1;
#             a.src = g;
#             m.parentNode.insertBefore(a, m)
#         })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');
#         ga('create', 'UA-47927501-1', 'auto');
#         ga('send', 'pageview');
#
#         $(document).ready(function () {
#
#             var mobile_webview = null;
#             if (mobile_webview || window.matchMedia('(display-mode: standalone)').matches) {
#                 var airportRegister = document.getElementById('airport-register');
#                 if (airportRegister) {
#                     airportRegister.classList.remove('d-none');
#                 }
#             }
#
#             $('#btnSearchBox').click(function (e) {
#                 var sw=0;
#                 $('.floating-input').removeClass('empty')
#                 $('.floating-label').removeClass('empty')
#                 $('.label-error').html('')
#                 var city = get('#frmSearch input[name="city"]');
#                 var hotelCode = get('#frmSearch input[name="hotelCode"]');
#                 var fromDate=get('#frmSearch input[name="fromDate"]')
#                 var toDate=get('#frmSearch input[name="toDate"]')
#                 if(city=="" && hotelCode=="" ){
#                     $('#select-city').addClass('empty')
#                     $('.city-floating-label-error').addClass('empty')
#                     $('.city-label-error').html('لطفا شهر را انتخاب نمایید')
#                     sw++;
#                 }
#                 if(fromDate==""){
#                     $('.departureDate').addClass('empty')
#                     $('.departureDateDetails').addClass('empty')
#                     sw++;
#                 }
#                 if(toDate==""){
#                     $('.returnDate').addClass('empty')
#                     $('.returnDateDetails').addClass('empty')
#                     sw++;
#                 }
#                 if (sw==0) {
#                     //$(this).html('<span>جستجو و رزرو هتل </span>');
#                     $('.floating-input').removeClass('empty')
#                     $('.floating-label').removeClass('empty')
#                     $('.label-error').html('')
#                     $('#frmSearch').submit();
#                 }
#             });
#             //lazyload();
#                         $(window).scroll(function () {
#                 if (($(window).scrollTop()) > ($('#enamad').offset().top - 600) && !$('#enamad').hasClass('loaded')) {
#                     $('#enamad').addClass('loaded');
#                     //$('#enamad').html("<a referrerpolicy='origin' target='_blank' href='https://trustseal.enamad.ir/?id=38389&Code=UAnfdasFlKaH5XnRw9nMebYPPBiUpouT'><img referrerpolicy='origin' src='https://trustseal.enamad.ir/logo.aspx?id=38389&Code=UAnfdasFlKaH5XnRw9nMebYPPBiUpouT' alt='' style='cursor:pointer' Code='UAnfdasFlKaH5XnRw9nMebYPPBiUpouT'></a>");
#                     //$('#enamad').html('<a referrerpolicy="origin" target="_blank" href="https://trustseal.enamad.ir/?id=38389&amp;Code=YksdgEeLE82RDu2XTPco"><img referrerpolicy="origin" src="https://Trustseal.eNamad.ir/logo.aspx?id=38389&amp;Code=YksdgEeLE82RDu2XTPco" alt="" style="cursor:pointer" id="YksdgEeLE82RDu2XTPco"></a>');
#                     //$('#samandehi').html('<img id=\'jxlzesgtesgtjxlznbqeapfujzpe\' style=\'cursor:pointer;width: 100%;\' onclick=\'window.open("https://logo.samandehi.ir/Verify.aspx?id=1001257&p=rfthobpdobpdrfthuiwkdshwjyoe", "Popup","toolbar=no, scrollbars=no, location=no, statusbar=no, menubar=no, resizable=0, width=450, height=630, top=30")\' alt=\'logo-samandehi\' src=\'https://logo.samandehi.ir/logo.aspx?id=1001257&p=nbpdlymalymanbpdodrfujynyndt\'/>');
#                 }
#             });
#                         $('#frmSubscribe input[name="subscribeEmail"]').focus(function () {
#                 $(this).attr('placeholder', 'ایمیل خود را وارد نمایید');
#             });
#
#         });
#
#         //fixme: this function not work correctlly and it should be checked
#         function emailSubscribe(obj) {
#             var txtBox = $('#frmSubscribe input[name="subscribeEmail"]');
#             $(obj).attr('disabled', true);
#             $(obj).html('<i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path></svg></i>');
#             $.ajax({
#                 url: '/تماس-با-هتلیار',
#                 cache: false,
#                 type: 'post',
#                 dataType: 'json',
#                 data: 'action=subscribe&token=110ae127c8c6f8a489b9faf7be089ee3fb02d9e6&' + $('#frmSubscribe').serialize(),
#                 success: function (server) {
#                     $(obj).attr('disabled', false);
#                     $(obj).html('<i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path></svg></i>');
#                     $(txtBox).val('');
#                     $(txtBox).attr('placeholder', server.msg);
#                 },
#                 error: function () {
#                     $(obj).attr('disabled', false);
#                     $(obj).html('<i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path></svg></i>');
#                     $(txtBox).val('');
#                     $(txtBox).attr('placeholder', 'لطفا مجددا سعی نمایید');
#                 }
#             });
#         }
#     </script>
#         <script src="https://hotelyar.com/static/plugin/slick-1.8.1/js/slick.min.js"></script>
#     <script src="https://hotelyar.com/static/plugin/slick-1.8.1/js/slick.min.js"></script>
#     <script src="https://hotelyar.com/static/plugin/lightgallery/lightgallery.min.js"></script>
#     <script src="https://hotelyar.com/static/plugin/lightgallery/plugins/zoom/lg-zoom.min.js"></script>
#     <script src="https://hotelyar.com/static/plugin/lightgallery/plugins/thumbnail/lg-thumbnail.min.js"></script>
#     <script src="https://hotelyar.com/static/js/custom_hotel_single.js?rnd=832"></script>
#     <script>
#         $(document).ready(function () {
#             dpConfig.since = '2025-2-2';
#             dpConfig.sinceTs = 1738441800000;
#             departureDate=datePicker.date(1738441800000);
#             dpConfig.to = '2025-2-3';
#             dpConfig.toTs = 1738528200000;
#             returnDate=datePicker.date(1738528200000);
#             dpConfig.listening='to';
#             dpConfig.span = 1738441800000;
#             dpConfig.selectPast = false;
#         });
#     </script>
#     <script>
#         var commentOffset = 0;
#         var lectureOffset = 0;
#         $(document).ready(function () {
#             $('#hotelSearchBoxBtn').click(function (e) {
#                 var sw=0;
#                 var fromDate=get('#hotelFrmSearch input[name="fromDate"]')
#                 var toDate=get('#hotelFrmSearch input[name="toDate"]')
#                 if(fromDate==""){
#                     $('.departureDate').addClass('empty')
#                     $('.departureDateDetails').addClass('empty')
#                     sw++;
#                 }
#                 if(toDate==""){
#                     $('.returnDate').addClass('empty')
#                     $('.returnDateDetails').addClass('empty')
#                     sw++;
#                 }
#                 if (sw==0) {
#                     $(this).html('<span>جستجوی مجدد </span><i class="spin"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M304 48C304 74.51 282.5 96 256 96C229.5 96 208 74.51 208 48C208 21.49 229.5 0 256 0C282.5 0 304 21.49 304 48zM304 464C304 490.5 282.5 512 256 512C229.5 512 208 490.5 208 464C208 437.5 229.5 416 256 416C282.5 416 304 437.5 304 464zM0 256C0 229.5 21.49 208 48 208C74.51 208 96 229.5 96 256C96 282.5 74.51 304 48 304C21.49 304 0 282.5 0 256zM512 256C512 282.5 490.5 304 464 304C437.5 304 416 282.5 416 256C416 229.5 437.5 208 464 208C490.5 208 512 229.5 512 256zM74.98 437C56.23 418.3 56.23 387.9 74.98 369.1C93.73 350.4 124.1 350.4 142.9 369.1C161.6 387.9 161.6 418.3 142.9 437C124.1 455.8 93.73 455.8 74.98 437V437zM142.9 142.9C124.1 161.6 93.73 161.6 74.98 142.9C56.24 124.1 56.24 93.73 74.98 74.98C93.73 56.23 124.1 56.23 142.9 74.98C161.6 93.73 161.6 124.1 142.9 142.9zM369.1 369.1C387.9 350.4 418.3 350.4 437 369.1C455.8 387.9 455.8 418.3 437 437C418.3 455.8 387.9 455.8 369.1 437C350.4 418.3 350.4 387.9 369.1 369.1V369.1z"/></svg></i>');
#                     $('#hotelFrmSearch').submit();
#                 }
#             });
#
#
#
#
#
#             $(".select-room").focus(function(e) {
#                 $(this).blur();
#             });
#
#             $('body').on('click','#frmComment #btnSaveComment',function () {
#                 var obj = this;
#                 var comment=$('#comment').val();
#                 var score=$('#score').val();
#                 //var code=$('#captcha').val();&& code.length>3
#                 if(comment.length>5 && score>0) {
#                     $(obj).attr('disabled', true);
#                     $(obj).html('<span>ثبت نظر</span><i><svg class="spin" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M449.9 39.96l-48.5 48.53C362.5 53.19 311.4 32 256 32C161.5 32 78.59 92.34 49.58 182.2c-5.438 16.81 3.797 34.88 20.61 40.28c16.97 5.5 34.86-3.812 40.3-20.59C130.9 138.5 189.4 96 256 96c37.96 0 73 14.18 100.2 37.8L311.1 178C295.1 194.8 306.8 223.4 330.4 224h146.9C487.7 223.7 496 215.3 496 204.9V59.04C496 34.99 466.9 22.95 449.9 39.96zM441.8 289.6c-16.94-5.438-34.88 3.812-40.3 20.59C381.1 373.5 322.6 416 256 416c-37.96 0-73-14.18-100.2-37.8L200 334C216.9 317.2 205.2 288.6 181.6 288H34.66C24.32 288.3 16 296.7 16 307.1v145.9c0 24.04 29.07 36.08 46.07 19.07l48.5-48.53C149.5 458.8 200.6 480 255.1 480c94.45 0 177.4-60.34 206.4-150.2C467.9 313 458.6 294.1 441.8 289.6z"/></svg></i>');
#                     $.ajax({
#                         url: 'https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز',
#                         cache: false,
#                         type: 'post',
#                         dataType: 'json',
#                         data: 'action=saveComment&token=110ae127c8c6f8a489b9faf7be089ee3fb02d9e6&' + $('#frmComment').serialize(),
#                         success: function (server) {
#                             //setCaptchaComment();
#                             $(obj).attr('disabled', false);
#                             $(obj).html('<span>ثبت نظر</span><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path></svg></i>');
#                             switch (server.result) {
#                                 case 'true':
#                                     alert(server.msg)
#                                     $('#frmComment')[0].reset();
#
#                                     break;
#                                 default:
#                                     alert(server.msg)
#                                     break;
#                             }
#                         },
#                         error: function () {
#                             $(obj).attr('disabled', false);
#                             $(obj).html('<span>ثبت نظر</span><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path></svg></i>');
#                             tryAgain();
#                         }
#                     });
#                 }else{
#                     alert('اطلاعات را به درستی پر نکرده اید');
#                 }
#             });
#
#             $.ajax({
#                 url: 'https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز',
#                 cache: false,
#                 type: 'post',
#                 dataType: 'html',
#                 data: 'action=load_comment_area&token=110ae127c8c6f8a489b9faf7be089ee3fb02d9e6',
#                 success: function (server) {
#                     $('.ajax-comment-body').html(server);
#                     $.fn.starrating = function(options) {
#                         var defaults = {
#                             rtl: false,
#                             onSelect: function(v){
#                                 return v;
#                             }
#                         };
#                         var settings = $.extend( {}, defaults, options );
#                         this.addClass("star-rating"+((settings.rtl)?"-rtl":""));
#                         this.html("<s><s><s><s><s></s></s></s></s></s>");
#                         this.children().on("click", function(e) {
#                             $(this).closest('div').find('.active').removeClass('active');
#                             $(e.target).parentsUntil("div").addClass('active');
#                             $(e.target).addClass('active');
#                             var numStars = $(e.target).parentsUntil("div").length+1;
#                             settings.onSelect(numStars);
#                         });
#                     };
#                     $("#my-rating-ltr").starrating({
#                         rtl:false,
#                         onSelect:function(res){
#                             $("#score").val(res);
#                             var scoreNames = [];
#                             scoreNames[1]='افتضاح';
#                             scoreNames[2]='کمتر از حد انتظار';
#                             scoreNames[3]='متوسط در حد انتظار';
#                             scoreNames[4]='خیلی خوب';
#                             scoreNames[5]='عالی و لذت بخش';
#                             $("#scorename").html(scoreNames[res]);
#                         }
#                     });
#                 },
#                 error: function () {}
#             });
#
#             if ($('#single-scroll').length) {
#                                 $('.more-text').css('height','250px');
#                 $('.more-text').css('overflow-y','scroll');
#                 $('.nav-tooltip').tooltip();
#                             }
#         });
#
#         var loadJS = function(url, implementationCode, location){
#             var scriptTag = document.createElement('script');
#             scriptTag.src = url;
#             scriptTag.onload = implementationCode;
#             scriptTag.onreadystatechange = implementationCode;
#             location.appendChild(scriptTag);
#         };
#         var yourCodeToBeCalled = function(){}
#
#         function showOnlinePackageModal(roomId) {
#             $('#onlinePackageModal tr[data-room-id="' + roomId + '"]').css('display', 'table-row');
#             $('#onlinePackageModal').modal('show');
#         }
#
#         function goBook() {
#             $('html, body').animate({
#                 scrollTop: $('#book').offset().top
#             }, 200);
#         }
#
#         function reserve(obj) {
#             var freeDayPackage = false;
#             var selectedRoomCount = 0;
#             $('.select-room').each(function () {
#                 selectedRoomCount += parseInt($(this).val());
#             });
#             if (freeDayPackage && selectedRoomCount > 1) {
#                 alert('کاربر گرامی با توجه به اینکه هتل در تاریخ درخواستی شما پکیج ویژه در نظر گرفته است، لطفا برای دریافت هدیه یک شب رایگان، رزرو خود را به صورت رزروهای تک اتاقی ثبت نمایید');
#             } else if (selectedRoomCount > 0) {
#                 $(obj).html('<span>اقدام به رزرو </span><i class="spin"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M304 48C304 74.51 282.5 96 256 96C229.5 96 208 74.51 208 48C208 21.49 229.5 0 256 0C282.5 0 304 21.49 304 48zM304 464C304 490.5 282.5 512 256 512C229.5 512 208 490.5 208 464C208 437.5 229.5 416 256 416C282.5 416 304 437.5 304 464zM0 256C0 229.5 21.49 208 48 208C74.51 208 96 229.5 96 256C96 282.5 74.51 304 48 304C21.49 304 0 282.5 0 256zM512 256C512 282.5 490.5 304 464 304C437.5 304 416 282.5 416 256C416 229.5 437.5 208 464 208C490.5 208 512 229.5 512 256zM74.98 437C56.23 418.3 56.23 387.9 74.98 369.1C93.73 350.4 124.1 350.4 142.9 369.1C161.6 387.9 161.6 418.3 142.9 437C124.1 455.8 93.73 455.8 74.98 437V437zM142.9 142.9C124.1 161.6 93.73 161.6 74.98 142.9C56.24 124.1 56.24 93.73 74.98 74.98C93.73 56.23 124.1 56.23 142.9 74.98C161.6 93.73 161.6 124.1 142.9 142.9zM369.1 369.1C387.9 350.4 418.3 350.4 437 369.1C455.8 387.9 455.8 418.3 437 437C418.3 455.8 387.9 455.8 369.1 437C350.4 418.3 350.4 387.9 369.1 369.1V369.1z"/></svg></i>');
#                 $('#frmReservation')[0].submit();
#
#                 setTimeout( function(){
#                     $(obj).html('<span>اقدام به رزرو </span>');
#                 }  , 1500 );
#             }
#             else {
#                 toastr.error('حداقل یک اتاق را انتخاب نمایید');
#             }
#         }
#
#         function loadComment(obj) {
#             $(obj).attr('disabled', true);
#             $(obj).css("background-color", "#77b2bd");
#
#             $(obj).html('<span>لطفا منتظر بمانید...</span><i><svg class="spin" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M449.9 39.96l-48.5 48.53C362.5 53.19 311.4 32 256 32C161.5 32 78.59 92.34 49.58 182.2c-5.438 16.81 3.797 34.88 20.61 40.28c16.97 5.5 34.86-3.812 40.3-20.59C130.9 138.5 189.4 96 256 96c37.96 0 73 14.18 100.2 37.8L311.1 178C295.1 194.8 306.8 223.4 330.4 224h146.9C487.7 223.7 496 215.3 496 204.9V59.04C496 34.99 466.9 22.95 449.9 39.96zM441.8 289.6c-16.94-5.438-34.88 3.812-40.3 20.59C381.1 373.5 322.6 416 256 416c-37.96 0-73-14.18-100.2-37.8L200 334C216.9 317.2 205.2 288.6 181.6 288H34.66C24.32 288.3 16 296.7 16 307.1v145.9c0 24.04 29.07 36.08 46.07 19.07l48.5-48.53C149.5 458.8 200.6 480 255.1 480c94.45 0 177.4-60.34 206.4-150.2C467.9 313 458.6 294.1 441.8 289.6z"/></svg></i>');
#             $.ajax({
#                 url: 'https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز',
#                 cache: false,
#                 type: 'post',
#                 data: "action=commentLoad&token=110ae127c8c6f8a489b9faf7be089ee3fb02d9e6&hotelCode=726&commentOffset=" + commentOffset,
#                 success: function (server) {
#                     $(obj).attr('disabled', false);
#                     $(obj).html('<span>مشاهده نظرات بیشتر</span><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M449.9 39.96l-48.5 48.53C362.5 53.19 311.4 32 256 32C161.5 32 78.59 92.34 49.58 182.2c-5.438 16.81 3.797 34.88 20.61 40.28c16.97 5.5 34.86-3.812 40.3-20.59C130.9 138.5 189.4 96 256 96c37.96 0 73 14.18 100.2 37.8L311.1 178C295.1 194.8 306.8 223.4 330.4 224h146.9C487.7 223.7 496 215.3 496 204.9V59.04C496 34.99 466.9 22.95 449.9 39.96zM441.8 289.6c-16.94-5.438-34.88 3.812-40.3 20.59C381.1 373.5 322.6 416 256 416c-37.96 0-73-14.18-100.2-37.8L200 334C216.9 317.2 205.2 288.6 181.6 288H34.66C24.32 288.3 16 296.7 16 307.1v145.9c0 24.04 29.07 36.08 46.07 19.07l48.5-48.53C149.5 458.8 200.6 480 255.1 480c94.45 0 177.4-60.34 206.4-150.2C467.9 313 458.6 294.1 441.8 289.6z"/></svg></i>');
#                     $('.btn-load').remove();
#                     if (server == '') {
#                         $(obj).hide();
#                     } else {
#                         server = server.replace(/HOTELNAMEKEY/g, 'هتل بزرگ شیراز');
#                         $('#comments-container').append(server);
#                         commentOffset +=10;
#                     }
#                 },
#                 error: function () {
#                     $(obj).attr('disabled', false);
#                     $(obj).html('<span>مشاهده نظرات بیشتر</span><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M449.9 39.96l-48.5 48.53C362.5 53.19 311.4 32 256 32C161.5 32 78.59 92.34 49.58 182.2c-5.438 16.81 3.797 34.88 20.61 40.28c16.97 5.5 34.86-3.812 40.3-20.59C130.9 138.5 189.4 96 256 96c37.96 0 73 14.18 100.2 37.8L311.1 178C295.1 194.8 306.8 223.4 330.4 224h146.9C487.7 223.7 496 215.3 496 204.9V59.04C496 34.99 466.9 22.95 449.9 39.96zM441.8 289.6c-16.94-5.438-34.88 3.812-40.3 20.59C381.1 373.5 322.6 416 256 416c-37.96 0-73-14.18-100.2-37.8L200 334C216.9 317.2 205.2 288.6 181.6 288H34.66C24.32 288.3 16 296.7 16 307.1v145.9c0 24.04 29.07 36.08 46.07 19.07l48.5-48.53C149.5 458.8 200.6 480 255.1 480c94.45 0 177.4-60.34 206.4-150.2C467.9 313 458.6 294.1 441.8 289.6z"/></svg></i>');
#                 }
#             });
#         }
#
#         function waitBook(obj, roomTypeCode) {
#             $('#frmWaitBook input[name="roomTypeCode"]').val(roomTypeCode);
#             $('#frmWaitBook')[0].submit();
#         }
#
#         function loadHotelPlace(code,MV){
#             /*$.ajax({
#                 url:'https://hotelyar.com/uiHotelProperty.php?hotelCode=726&hotelDistancePlaceCode='+code+'&action=loadHotelPlace',
#                 type:'post',
#                 cache:false,
#                 success:function(server){
#                     if(MV){
#                         $('#hotelPlaceModalBody').html(server);
#                         $('#hotelPlaceModal').modal('show');
#
#                     }else{
#                         $('#loadHotelPlace').html(server);
#                     }
#
#                 },
#                 error:function(){
#                     alert('لطفا مجددا سعی نمایید');
#                 }
#             });*/
#         }
#
#         function loadLecture(obj) {
#             $(obj).attr('disabled', true);
#             $(obj).html('<span>نمایش بیشتر</span><i class="spin"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M255.9 32.11c79.47 0 151.8 41.76 192.1 109.4V48C448 39.16 455.2 32 464 32S480 39.16 480 48v128C480 184.8 472.8 192 464 192h-128C327.2 192 320 184.8 320 176S327.2 160 336 160h85.85C387.5 100.7 324.9 64 256 64C150.1 64 64 150.1 64 256s86.13 192 192 192c59.48 0 114.7-26.91 151.3-73.84c5.438-7 15.48-8.281 22.47-2.75c6.953 5.438 8.187 15.5 2.75 22.44c-42.8 54.75-107.3 86.05-176.7 86.05C132.4 479.9 32 379.5 32 256S132.4 32.11 255.9 32.11z"/></svg></i>');
#             lectureOffset++;
#             $.ajax({
#                 url: 'https://hotelyar.com/hotel/726/هتل-بزرگ-شیراز',
#                 cache: false,
#                 type: 'post',
#                 data: "action=lecture&token=110ae127c8c6f8a489b9faf7be089ee3fb02d9e6&hotelCode=726&lectureOffset=" + lectureOffset,
#                 success: function (server) {
#                     $(obj).attr('disabled', false);
#                     $(obj).html('<span>نمایش بیشتر</span><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path></svg></i>');
#                     if (server == '') {
#                         $(obj).hide();
#                     } else {
#                         server = server.replace(/HOTELNAMEKEY/g, 'هتل بزرگ شیراز');
#                         $('#lecture-container').append(server);
#                     }
#                 },
#                 error: function () {
#                     $(obj).attr('disabled', false);
#                     $(obj).html('<span>نمایش بیشتر</span><i><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M148.7 411.3l-144-144C1.563 264.2 0 260.1 0 256s1.562-8.188 4.688-11.31l144-144c6.25-6.25 16.38-6.25 22.62 0s6.25 16.38 0 22.62L54.63 240H496C504.8 240 512 247.2 512 256s-7.156 16-16 16H54.63l116.7 116.7c6.25 6.25 6.25 16.38 0 22.62S154.9 417.6 148.7 411.3z"></path></svg></i>');
#                 }
#             });
#         }
#         function showPlusMinusBtn(roomId){
#             $('#roomPlusMinus'+roomId).removeClass('d-none');
#             $('#roomBtn'+roomId).addClass('d-none');
#         }
#     </script>
#     </body>
#     </html>
# """
# ###hotelyar.com
#
# soup = BeautifulSoup(data, 'html.parser')
# print(soup.select_one('.ss-hotel-single-hhwt-name').text)  # name
# print(soup.select_one('div.color-gray:nth-child(2) > span:nth-child(1)').text)  # address
# print(soup.select_one(
#     'div.ss-hotel-single-h-header-features-item:nth-child(3) > div:nth-child(2) > span:nth-child(2)').text)  # room count
# print(soup.select_one(
#     'div.ss-hotel-single-h-header-features-item:nth-child(4) > div:nth-child(2) > span:nth-child(2)').text)  # high
# for item in soup.select('.ss-reserve-table > tbody:nth-child(2) tr'):
#     print(item.select_one('td:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)').text)  # price
#     print(item.select_one('td:nth-child(6) > span:nth-child(2)').text)  # price
#     print(item.select_one('td:nth-child(4) > div:nth-child(1)').text)  # discount
#     print('*' * 30)
#
# for item in soup.select('#comments-container>div'):
#     print(item.select_one(
#         'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)').text)  # username
#     print(item.select_one(
#         'div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)').text)  # score
#     print(item.select_one('div:nth-child(2) > p:nth-child(1)').text)  # text
#     print('&' * 30)
#
