import thu_vien as tv
import streamlit as st
import pandas as pd



dta=tv.connect_google("1ZGJ94U_I6iOb-ZInoZWTrHH4Ih7aA-ynlnrT8yR5yh8")
#dta.sheet1.get_all_cells()
# print(dta.sheet1)
#  = ["cot 1","cột 2","cột 3","cột 4"]
# .sheet1.append_row(row)
# dta2=dta.sheet1.get_all_records()
# print(dta2)
st.set_page_config(page_title="📋 SỔ NHỰA",page_icon="🤣",layout="wide")

st.title("📋 SỔ NHỰA")
col1, col2, col3 = st.columns(3)
with col1:
    # zone= st.text_input("🔎 Line nào")
    zone = st.selectbox("🔎 Line nào",["Line 1","Line 2","Line 3","Line 4","Line 5","Line 6","Line 7"],index=5)
with col2:
    # may = st.text_input("🔎 Nhập máy vào")
    may = st.selectbox("🔎 Máy nào",["Máy 1","Máy 2","Máy 3","Máy 4","Máy 5","Máy 6"])
with col3:
    ws_mahang = dta.worksheet("Mahang")
    ds_mahang = ws_mahang.col_values(1)[1:]
#    for mahang in dta.worksheets("Mahang"):
#        ma_hang = mahang.col_values(1)[1:]
    ma_hang = st.selectbox("🔎 Mã hàng",ds_mahang)
col4, col5, col6 = st.columns(3)
with col4:
    ten_khuon = st.text_input("📋 Nhập tên Khuôn")
with col5:
    trai_phai = st.selectbox(" 🤚🏻 Bên tái hay phải ✋🏻",["T","P"])
with col6:
# sửa code để test (dòng sau này sai)
    trong_luong = st.text_input("📋 Nhập số nhựa")
# code đúng khi chạy
#    trong_luong = st.number_input("📋 Nhập số nhựa",min_value=1,max_value=900,value= None)

# pre_data = f"{zone},{may},{ten_khuon},{trong_luong}"
#pre_data = [zone,may,ten_khuon,trong_luong]

if st.button("💾 Lưu"):
    record = dta.sheet1.get_all_records()
    if len(record) == 0:
        tieu_de_cot = ["Zone","May","MaHang","TenKhuon","Ben","TrongLuong"]
        dta.sheet1.append_row(tieu_de_cot)
        row = [zone, may ,ma_hang, ten_khuon, trai_phai, trong_luong]
        dta.sheet1.append_row(row)
    else:
        row = [zone, may ,ma_hang, ten_khuon, trai_phai, trong_luong]
        dta.sheet1.append_row(row)
    #st.success("✅ Đã lưu thành công")
    st.toast("✅ Đã lưu thành công")
record = dta.sheet1.get_all_records()
#col6, col7 = st.columns(2)

bangnhua_t, bangnhua_p = st.columns(2)
with bangnhua_t:
    if  len(record) > 0:
        df = pd.DataFrame(record)
        loc_trai=df[
            (df["Zone"]==zone)
            &
            (df["Ben"]== "T")
            &
            (df["May"]==may)
            &
            (df["MaHang"]== ma_hang)
        ]
        loc_trai = loc_trai[["TenKhuon","TrongLuong"]]
        st.dataframe(loc_trai)
with bangnhua_p:
    if  len(record) > 0:
        df = pd.DataFrame(record)
        loc_phai=df[
            (df["Zone"]==zone)
            &
            (df["Ben"]== "P")
            &
            (df["May"]==may)
            &
            (df["MaHang"]== ma_hang)
        ]
        loc_phai = loc_phai[["TenKhuon","TrongLuong"]]
        st.dataframe(loc_phai)

# Đoạn code lấy thông tin từ Dataframe lên form nhập



#st.write(df["MaHang"].unique())
#st.write(repr(ma_hang))
