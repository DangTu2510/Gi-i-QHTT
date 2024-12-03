from tkinter import *
from tkinter import ttk
import numpy as np

root = Tk()
root.title('Giải bài toán quy hoạch tuyến tính')
#cài đặt cửa sổ
root.minsize(height=720, width=1080)

# Thêm thanh cuộn
scrollbar = Scrollbar(root, orient="vertical")

# Tạo Canvas
canvas = Canvas(root, yscrollcommand=scrollbar.set, width=1060, height=1500)
canvas.place(x = 0, y = 0)

# Kết nối thanh trượt với Canvas
scrollbar.config(command=canvas.yview)
scrollbar.pack(side="right", fill="y")

frame = Frame(canvas, height=2500, width=1060)
def Tao_Frame(height1):
    # Tạo Frame bên trong Canvas
    frame = Frame(canvas, height=2500, width=1060)
    canvas.create_window((0,height1), window=frame, anchor="nw")
    return frame

def on_configure(event):
    my_canvas.configure(scrollregion=my_canvas.bbox("all"))

# Gắn sự kiện cho canvas khi thay đổi kích thước
#my_canvas.bind('<Configure>', on_configure)

#các biến
so_bien = IntVar()
so_rang_buoc = IntVar()
#hàm ràng buộc nhập số cho Entry
def on_validate_input(P):
    # Hàm kiểm tra nhập liệu để chỉ chấp nhận giá trị số
    if P == "" or P.replace("-", "").isdigit():
        return True
    else:
        return False
# Tạo một hàm kiểm tra nhập liệu để chỉ chấp nhận giá trị số
validate_input = root.register(on_validate_input)
#đưa bài toán về dạng đánh thuế
def ppDanhThue(A, b, c, J, xj, cj, frame2):
  import copy
  m = len(A) # Số hàng của A
  n = len(A[0]) # Số cột của A

  # Bảng đơn hình thứ nhất
  import pandas as pd
  # 3 cột đầu
  x = {'J' : J,
       'cj' : cj,
       'xj' : xj}
  a = pd.DataFrame(x)
  # Các cột c
  for i in range(n):
    name = 'c' + str(i+1)
    a[name] = pd.Series([row[i] for row in A])
  # Tính delta k : Coi M = 0
  delta_k = ['x', 'x', 'x']
  for x in range(n):
    s = 0
    if (x+1) in J:
      s = 0
    else:
      for i in range(len(cj)):
        if cj[i] == 'M':
          cjm = 0
          s += cjm * A[i][x]
        else:
          s += cj[i] * A[i][x]
      s = s - c[x]
    delta_k.append(s)
  a.loc[m] = delta_k
  # Tính delta k(P) : Coi M = 1, C = 0
  delta_kP = ['x', 'x', 'x']
  for x in range(n):
    s = 0
    if (x+1) in J:
      s = 0
    else:
      for i in range(len(cj)):
        if cj[i] == 'M':
          cjm = 1
          s += cjm * A[i][x]
        else:
          s += cj[i] * A[i][x]
    delta_kP.append(s)
  a.loc[m + 1] = delta_kP
  print(a)
  arows, acols = a.shape
  ten_cot = a.columns
  ten_cot = list(ten_cot)
  print(ten_cot)
  height = 0
  weight = 30
  Label(frame2, text="Lập bảng đơn hình: ", font=('Times New Roman', 14)).place(x = weight, y = height)
  for i in range(len(ten_cot)):
      Label(frame2, text=f'{ten_cot[i]}', font=('Times New Roman', 12), width=3, bg='white').place(x=weight, y= height + 30)
      weight += 35
  weight = 30
  for i in range(len(ten_cot)):
      if i < 3:
          Label(frame2, text='', font=('Times New Roman', 12), width=3, bg='white').place(x=weight, y= height + 55)
      else:
          Label(frame2, text=f'{c[i - 3]}', font=('Times New Roman', 12), width=3, bg='white').place(x=weight, y=height + 55)
      weight += 35
  height += 80
  for i in range(arows):
      weight = 30
      for j in range(acols):
          if a.loc[i][j] == 'x':
              Label(frame2, text='', font=('Times New Roman', 12), width=3, bg='white').place(x=weight,y=height)
          else:
              Label(frame2, text=f'{a.loc[i][j]}', font=('Times New Roman', 12), width=3, bg='white').place(x = weight, y = height)
          weight += 35
      height += 25
  height1 = 80
  while True:
    int_delta_k = [s for s in delta_k if s != 'x']
    int_delta_kP = [s for s in delta_kP if s != 'x']
    # Tìm s
    s = -1
    for i in range(len(int_delta_k)):
      if int_delta_kP[i] > 0 and int_delta_kP[i] == max(int_delta_kP):
        max_value = max(int_delta_kP)
        max_index = []
        for j in range(len(int_delta_kP)):
          if(lambda x : x == max_value)(int_delta_kP[j]):
            max_index.append(j)
        if len(max_index) == 1:
          s = i
          break
        if int_delta_k[i] == max(int_delta_k):
          s = i
          break
      if int_delta_kP[i] == 0 and int_delta_k[i] > 0 and int_delta_k[i] == max(int_delta_k):
        s = i
    if s == -1:
      break

    # Tìm r
    name = 'c' + str(s + 1)
    int_cs = a[name][0:m]
    for i in range(len(int_cs)):
      if int_cs[i] > 0:
        min_value = xj[i] / int_cs[i]
        min_index = i
        break
    for i in range(len(xj)):
      if int_cs[i] > 0:
        if (lambda x, y: x/y)(xj[i], int_cs[i]) < min_value:
          min_value = (lambda x, y: x/y)(xj[i], int_cs[i])
          min_index = i
    r = min_index

    # Phần tử xoay
    name = 'c' + str(s + 1)
    z_sr = a[name][r]
    for i in range(arows):
        weight = 30
        for j in ten_cot:
            if i == 0 and j == name:
                Label(frame2, text=f'{a.loc[i][j]}', font=('Times New Roman', 12), width=3, bg='white', fg='red').place(x=weight, y=height1)
            weight += 35
        height1 += 25

    # Kiểm tra giảm vô hạn
    if z_sr <= 0:
      break

    # Đổi giá trị trong A_next
    A_next = copy.deepcopy(A)
    A_next.append(int_delta_k)
    A_next.append(int_delta_kP)
    A_new = copy.deepcopy(A_next)
    for i in range(len(A_next)):
      for j in range(len(A_next[0])):
        gtA = A_next[i][j]
        gtB = A_next[i][s]
        gtC = A_next[r][j]
        A_new[i][j] = gtA - (gtB * gtC) / z_sr
    for j in range(len(A_next[0])):
      A_new[r][j] = A_next[r][j] / z_sr
    for i in range(len(A_next)):
      if i == r:
        A_new[i][s] = 1
      else:
        A_new[i][s] = 0

    # xj và cj
    J[r] = s + 1
    cj[r] = c[s]
    xj_new = copy.deepcopy(xj)
    for i in range(len(xj_new)):
      if i == r:
        xj_new[i] = xj[i] / z_sr
      else:
        xj_new[i] = xj[i] - (xj[r] * A[i][s]) / z_sr
    xj = copy.deepcopy(xj_new)

    # Giá trị A
    A = copy.deepcopy(A_new)
    A.pop()
    A.pop()

    # Bảng đơn hình
    x = {'J' : J,
         'cj' : cj,
         'xj' : xj}
    a = pd.DataFrame(x)
    # Các cột c
    for i in range(n):
      name = 'c' + str(i+1)
      a[name] = pd.Series([row[i] for row in A])
    # Dòng delta k
    delta_k = ['x', 'x', 'x']
    delta_k.extend(A_new[len(cj)][:])
    a.loc[m] = delta_k
    # Dòng delta kP
    delta_kP = ['x', 'x', 'x']
    delta_kP.extend(A_new[len(cj) + 1][:])
    a.loc[m + 1] = delta_kP
    a = a.round(1)
    for i in range(arows):
        weight = 30
        for j in range(acols):
            if a.loc[i][j] == 'x':
                Label(frame2, text='', font=('Times New Roman', 12), width=3, bg='white').place(x=weight, y=height)
            elif a.loc[i][j] == "M":
                Label(frame2, text=f'{a.loc[i][j]}', font=('Times New Roman', 12), width=3, bg='white').place(x=weight, y=height)
            else:
                Label(frame2, text=f'{round(a.loc[i][j], 2)}', font=('Times New Roman', 12), width=3, bg='white').place(x=weight, y=height)
            weight += 35
        height += 25

  # Kết quả
  if z_sr <= 0:
    return -1
  else:
    x = [0] * len(c)
    xk = list(zip(J, xj))
    for i in range(len(J)):
      x[xk[i][0] - 1] = xk[i][1]
    x = [round(i, 3) for i in x]
    return x, height
def timCoSo(A, b, c, J, xj, cj):
  m = len(A) # Số hàng của A
  n = len(A[0]) # Số cột của A

  # Ma trận đơn vị
  I = []
  for i in range(m):
    row = []
    for j in range(m):
      if i == j:
        row.append(1)
      else:
        row.append(0)
    I.append(row)

  # Các cột của A
  column = []
  for j in range(n):
    column_x = [A[i][j] for i in range(m)]
    column.append(column_x)

  # Vecto J, cj và xj
  for i in range(len(I)):
    gtri = b[i]
    for j in range(len(column)):
      if column[j] == I[i]:
        xj.append(gtri)
        J.append(j + 1)
        cj.append(c[j])
  return J, xj, cj
def dangDanhThue(A, b, c):
  m = len(A) # Số hàng của A
  n = len(A[0]) # Số cột của A

  # Đổi dấu b -
  for i in range(len(b)):
    if b[i] < 0:
      for j in range(len(A[0])):
        A[i][j] = -A[i][j]
      b[i] = -b[i]

  # Ma trận đơn vị
  I = []
  for i in range(m):
    row = []
    for j in range(m):
      if i == j:
        row.append(1)
      else:
        row.append(0)
    I.append(row)

  # Các cột của A
  column = []
  for j in range(n):
    column_x = [A[i][j] for i in range(m)]
    column.append(column_x)

  # Tìm xem trong A có vecto đơn vị chưa
  in_I = []
  for i in column:
    if i in I:
      for j in range(len(I)):
        if I[j] == i:
          in_I.append(j)

  # Thêm vào các vecto còn thiếu
  for i in range(len(I)):
    if i not in in_I:
      new_column = I[i]
      for j in range(len(A)):
        A[j].append(new_column[j])
      c.append('M')
  return A, b, c
def Submit2(a, vecto_b, vecto_c, muc_tieu_fx, dau_bdt, height):
    #xử lý ma trận a
    A = []
    for i in range(len(dau_bdt)):
        Ai = [aij.get() for aij in a[i]]
        A.append(Ai)
    c = [ci.get() for ci in vecto_c]
    b = [bi.get() for bi in vecto_b]
    muc_tieu = muc_tieu_fx.get()
    list_bdt = [bdt.get() for bdt in dau_bdt]

    so_x = len(c)
    c_ban_dau = list(map(lambda x: x, c))
    #Xử lý đưa về dạng chính tắc
    m = len(A)  # Số hàng của A
    n = len(A[0])  # Số cột của A

    # Các cột của A
    column = []
    for j in range(n):
        column_x = [A[i][j] for i in range(m)]
        column.append(column_x)

    # Thành dấu =
    for i in range(len(list_bdt)):
        if list_bdt[i] == '<=':
            new_column = [0] * m
            new_column[i] = 1
            for j in range(len(A)):
                A[j].append(new_column[j])
            c.append(0)
        if list_bdt[i] == '>=':
            new_column = [0] * m
            new_column[i] = -1
            for j in range(len(A)):
                A[j].append(new_column[j])
            c.append(0)
    list_bdt = ['='] * m

    # Thay đổi max -> min
    if muc_tieu == 'Max':
        for i in range(len(c)):
            c[i] = -c[i]
        muc_tieu = 'Min'
    #tạo frame cho phần giải bài toán
    frame2 = Tao_Frame(height + 180)
    #Đưa về dạng đánh thuế
    A, b, c = dangDanhThue(A, b, c)
    #Tìm cơ số J, xj, cj
    J = []
    xj = []
    cj = []
    J, xj, cj = timCoSo(A, b, c, J, xj, cj)
    x, height = ppDanhThue(A, b, c, J, xj, cj, frame2)

    if (isinstance(x, int)) == True:
        Label(frame2, text=f"Bài toán không có phương án tối ưu", font=('Times New Roman', 14)).place(x = 400, y = height + 70)
    else:
        T = True
        for i in range(len(c)):
            if c[i] == 'M' and x[i] != 0:
                Label(frame2, text=f"Bài toán không có phương án tối ưu", font=('Times New Roman', 14)).place(x = 400, y = height + 70)
                T = False
                break
        if T == True:
            x_tu = x[0:so_x]
            Label(frame2, text=f"Phương án tối ưu của bài toán ban đầu: {x_tu}", font=('Times New Roman', 14)).place(x = 400, y = height + 70)
            f = 0
            for i in range(so_x):
                f += c_ban_dau[i] * x_tu[i]
            Label(frame2, text=f"Giá trị f(x) = {f}", font=('Times New Roman', 14)).place(x=400, y=height + 100)
    button_lam_moi = Button(frame, text="Làm bài mới", font=('Times New Roman', 10),
                            width=10, height=1,
                            command=lambda : Tao_Frame(180)).place(x=500, y=130)
def Submit1(frame1):
    # Xây dựng hàm mục tiêu
    n1 = so_bien.get()
    n2 = so_rang_buoc.get()
    title1 = Label(frame1, text="Hàm mục tiêu: ", font=('Times New Roman', 12)).place(x = 30, y = 0)
    fx = Label(frame1, text="f(x) = ", font=('Times New Roman', 12)).place(x=30, y=30)
    width_c = 80
    width_x = 120
    c_node_list = []
    for i in range(n1):
        ci = IntVar()
        c_node = Entry(frame1, width=6, font=("Times New Roman", 10),
                  validate="key",
                  textvariable=ci).place(x = width_c, y = 30)
        xi = Label(frame1, text=f'x_{i + 1}', font=('Times New Roman', 12)).place(x= width_x, y = 30)
        width_c += 85
        width_x += 85
        c_node_list.append(ci)
    option1 = ["Min", "Max"]
    select_option = StringVar()
    mui_ten = Label(frame1, text="----  >", font=('Times New Roman', 10)).place(x = width_x - 45, y = 30)
    muc_tieu = ttk.Combobox(frame1, font=('Times New Roman', 10), width=10,
                            textvariable=select_option,
                            state="readonly",
                            values=option1).place(x = width_x + 20, y = 30)

    #Xây dựng hàm ràng buộc
    a = []
    b = []
    height = 100
    dau_b = []
    title2 = Label(frame1, text="Các ràng buộc: ", font=('Times New Roman', 12)).place(x = 30, y = 70)
    for i in range(n2):
        select_option2 = StringVar()
        option2 = ["=", ">=", "<="]
        width_c = 80
        width_x = 120
        ai = []
        b_value = IntVar()
        for j in range(n1):
           aij = IntVar()
           aij_node = Entry(frame1, width=6, font=("Times New Roman", 10),
                  validate="key",
                  textvariable=aij).place(x = width_c, y = height)
           xi = Label(frame1, text=f'x_{j + 1}', font=('Times New Roman', 12)).place(x=width_x, y=height)
           ai.append(aij)
           width_c += 85
           width_x += 85
        dau = ttk.Combobox(frame1, font=('Times New Roman', 10), width= 5,
                           textvariable=select_option2,
                           state="readonly",
                           values=option2).place(x = width_x - 30, y = height)
        node_b = Entry(frame1, width=6, font=('Times New Roman', 10),
                       validate="key",
                       textvariable=b_value).place(x = width_x + 50, y=height)
        dau_b.append(select_option2)
        height += 25
        b.append(b_value)
        a.append(ai)
    button2 = Button(frame1, text="Giải", font=('Times New Roman', 10),
                 width=10, height=1,
                 command=lambda : Submit2(a, b, c_node_list, select_option, dau_b, height + 80)).place(x = 350, y = height + 40)

#Nhập số biến của hàm mục tiêu và số ràng buộc
tieu_de = Label(frame, text='ỨNG DỤNG GIẢI BÀI TOÁN QUY HOẠCH TUYẾN TÍNH',
                fg='red', font=('cambria, 16'), width = 50).place(x = 250, y = 10)
yeu_cau_1 = Label(frame, text='Nhập số biến của bài toán: ',
                fg='black', font=('cambria, 10'), width=30).place(x=10, y=80)
o_so_bien = Entry(frame, width=5, font=("Times New Roman", 10),
                validate="key",
                validatecommand=(validate_input, "%P"),
                textvariable=so_bien).place(x=250, y=80)
yeu_cau_2 = Label(frame, text='Nhập số ràng buộc của bài toán: ',
                fg='black', font=('cambria, 10'), width=30).place(x=10, y=100)
o_so_rang_buoc = Entry(frame, width=5, font=("Times New Roman", 10),
                validate="key",
                validatecommand=(validate_input, "%P"),
                textvariable=so_rang_buoc).place(x=250, y=100)

button1 = Button(frame, text="Xác nhận", font=('Times New Roman', 10),
                 width=10, height=1,
                 command=lambda : Submit1(Tao_Frame(180))).place(x = 350, y = 130)

canvas.create_window((0, 0), window=frame, anchor="nw")

# Thiết lập scrollregion cho Canvas
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))
root.mainloop()