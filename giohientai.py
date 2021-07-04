import cv2
import numpy as np
import time
import serial #thu vien ket noi voi arduimo
import xlwt #thu vien doc ghi file excel
import datetime

sta = time.time()
rong_min=80 # chieu rong toi thieu hinh chu nhat
cao_min=80 #chieu cao toi thieu hinh chu nhat

offset=6 # so pixel sai so nhan biet cho phep 

tungdoduong=550 #vi tri gan diem nhan dien

delay= 60 #FPS nguon nhan
# khai bao cac bien dung trong chuong trinh
detec = []
biendem=0
dem=0
doiso=0
so_xe= 0

# tao cac trang tinh va ghi tieu de cot
wb = xlwt.Workbook()
sheet1 = wb.add_sheet('sheet 1')
sheet2 = wb.add_sheet('sheet 2')
sheet3 = wb.add_sheet('sheet 3')
sheet1.write(0, 0, 'STT')
sheet1.write(0, 1, 'Thoi gian ghi nhan')
sheet1.write(0, 2, 'So phuong tien ghi nhan')
sheet1.write(0, 3, 'mat do phuong tien ghi nhan')



#dinh nghi tinh tam hinh chu nhat
def tam_chu_nhat(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

#nguon vao video
cap = cv2.VideoCapture('C:\\Users\\Admin\\Desktop\\video.mp4')
tru_nen = cv2.bgsegm.createBackgroundSubtractorMOG()   # ham xoa nen 

while True:

   
    ret , frame1 = cap.read()
    
    
    
    biendem=biendem + 1
    tempo = float(1/delay)
    time.sleep(tempo)
    # xu ly anh
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    img_sub = tru_nen.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
    dilatada = cv2.morphologyEx (dilatada, cv2. MORPH_CLOSE , kernel)
    
    # tim duong vien
    contorno,h=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # ve duong thang de xac dinh so xe di qua
    cv2.line(frame1, (25, tungdoduong), (1200, tungdoduong), (255,127,0), 3) 
    for(i,c) in enumerate(contorno):
        # gan toa do hinh bao quanh chuyen dong
        (x,y,w,h) = cv2.boundingRect(c)
        # dieu kien de duoc nhan dien la o to
        validar_contorno = (w >= rong_min) and (h >= cao_min)
        if not validar_contorno:
            continue
        # ve hinh chu nhat voi toa do da biet
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)        
        tam = tam_chu_nhat(x, y, w, h) # xac dinh tam
        
        detec.append(tam) # thêm một phân tử vào danh sách hiên tại
        cv2.circle(frame1, tam, 4, (0, 0,255), -1) # ve 1 cham o tam hinh chu nhat

        for (x,y) in detec:
            # khi o to di chuyen qua duong dinh san, cong 1 vao bien dem
            if y<(tungdoduong+offset) and y>(tungdoduong-offset):
                so_xe+=1
               

                cv2.line(frame1, (25, tungdoduong), (1200, tungdoduong), (0,127,255), 3)  
                detec.remove((x,y))
              
                print("car is detected : "+str(so_xe))        
          
    cv2.putText(frame1, "VEHICLE COUNT : "+str(so_xe), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
    cv2.imshow("Video Original" , frame1)
    #moi 180 vong lam ghi du lieu 1 lan
    thoigian=biendem*1/60
    if thoigian==3:
        sto = time.time()
        end =sto-sta
        matdo = float(so_xe-doiso)/end
        
        dem=dem+1
        sheet1.write(dem,0,dem)
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        sheet1.write(dem, 1, current_time)
        sheet1.write(dem, 2, so_xe)
        sheet1.write(dem, 3, matdo)
        doiso=so_xe
        sta=sto
            
            
        wb.save('C:\\Users\\Admin\\Desktop\\python\\aanh.xls')
        biendem=0
    #print(thoigian)
   # cv2.imshow("Detectar",dilatada)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
cap.release()
