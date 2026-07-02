import thu_vien as tv
import streamlit as st
import pandas as pd



dta=tv.connect_google("1ZGJ94U_I6iOb-ZInoZWTrHH4Ih7aA-ynlnrT8yR5yh8")
#dta.sheet1.get_all_cells()
st.set_page_config(page_title="📋 SỔ NHỰA",page_icon="🤣",layout="wide")
st.title("📋 SỔ NHỰA")
col1, col2, col3 = st.columns(3)
with col1:
    zone = st.selectbox("🔎 Line nào",["Line 1","Line 2","Line 3","Line 4","Line 5","Line 6","Line 7"],index=5)
with col2:
    # may = st.text_input("🔎 Nhập máy vào")
    may = st.selectbox("🔎 Máy nào",["Máy 1","Máy 2","Máy 3","Máy 4","Máy 5","Máy 6"])
with col3:
    ws_mahang = dta.worksheet("Mahang")
    ds_mahang = ws_mahang.col_values(1)[1:]
    ma_hang = st.selectbox("🔎 Mã hàng",ds_mahang)
col4, col5, col6 = st.columns(3)
with col4:
    ten_khuon = st.text_input("📋 Nhập tên Khuôn")
with col5:
    trai_phai = st.selectbox(" 🤚🏻 Khuôn bên nào",["T","P"])
with col6:
    trong_luong = st.number_input("📋 Nhập số nhựa",min_value=1.0,max_value=900.0,value= None)
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

st.write(record[-1]["TrongLuong"])
st.write(type(record[-1]["TrongLuong"]))
st.write(repr(record[-1]["TrongLuong"]))


if  (len(record) > 0) & (trai_phai == "T"):
    df = pd.DataFrame(record)
    loc=df[
        (df["Zone"]==zone)
        &
        (df["Ben"]== "T")
        &
        (df["May"]==may)
        &
        (df["MaHang"]== ma_hang)
    ]
    loc = loc[["TenKhuon","TrongLuong"]]
    loc = loc.rename(columns={
        "TenKhuon": "Tên khuôn trái",
        "TrongLuong": "Số nhưa trái"
    })
else:
    df = pd.DataFrame(record)
    loc = df[
        (df["Zone"] == zone)
        &
        (df["Ben"] == "P")
        &
        (df["May"] == may)
        &
        (df["MaHang"] == ma_hang)
        ]
    loc = loc[["TenKhuon", "TrongLuong"]]
    loc = loc.rename(columns={
        "TenKhuon": "Tên khuôn phải",
        "TrongLuong": "Số nhưa phải"
    })
st.dataframe(loc,hide_index=True,use_container_width=True)
