import thu_vien as tv
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
#-------------------

dta=tv.connect_google("1ZGJ94U_I6iOb-ZInoZWTrHH4Ih7aA-ynlnrT8yR5yh8")

#--------------------------

st.set_page_config(
    page_title="📋 SỔ NHỰA",
    layout="wide"
)

# ===== Khởi tạo session_state =====
if "id" not in st.session_state:
    st.session_state["id"] = None

if "zone" not in st.session_state:
    st.session_state["zone"] = ""

if "may" not in st.session_state:
    st.session_state["may"] = ""

if "mahang" not in st.session_state:
    st.session_state["mahang"] = ""

if "trai_phai" not in st.session_state:
    st.session_state["trai_phai"] = ""

if "tenkhuon" not in st.session_state:
    st.session_state["tenkhuon"] = ""

if "nhua" not in st.session_state:
    st.session_state["nhua"] = 0.0
# ================================

# Các đoạn code còn lại...

st.title("📋 SỔ NHỰA")
with st.expander("➕ Chọn khuôn cần tìm"):

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        zone = st.selectbox("🔎 Line nào", ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5", "Line 6", "Line 7"],
                            index=5)
    with col2:
        # may = st.text_input("🔎 Nhập máy vào")
        may = st.selectbox("🔎 Máy nào", ["Máy 1", "Máy 2", "Máy 3", "Máy 4", "Máy 5", "Máy 6"],index=4)
    with col3:
        ws_mahang = dta.worksheet("Mahang")
        ds_mahang = ws_mahang.col_values(1)[1:]
        ma_hang = st.selectbox("🔎 Mã hàng", ds_mahang)
    with col4:
        trai_phai = st.selectbox(" 🤚🏻 Khuôn bên nào", ["T", "P"], index=0)
    with col5:
        ten_khuon = st.text_input("📋 Nhập tên Khuôn").upper()

    with col6:
        trong_luong = st.number_input("📋 Nhập số nhựa", min_value=1.0, max_value=900.0, value=None)

    if st.button("💾 Lưu"):
        record = dta.sheet1.get_all_records()
        df = pd.DataFrame(record)

        if df.empty:
            new_id = 1
        else:
            max_id = df["ID"].max()
            new_id = int(max_id) + 1

        if trai_phai == "T":
            ben = "bên trái"
        else:
            ben = "bên phải"

       # st.write(new_id)


        if len(record) == 0:
            tieu_de_cot = ["ID","Zone","May","MaHang","TenKhuon","Ben","TrongLuong"]
            dta.sheet1.append_row(tieu_de_cot)
            row = [new_id,zone, may ,ma_hang, ten_khuon, trai_phai, trong_luong]
            dta.sheet1.append_row(row)
        else:
            row = [new_id,zone, may ,ma_hang, ten_khuon, trai_phai, trong_luong]
            dta.sheet1.append_row(row)
        #st.success("✅ Đã lưu thành công")
        st.toast(f"✅ Đã lưu thành công khuôn {ten_khuon} {ben}")
        record = dta.sheet1.get_all_records()
        df = pd.DataFrame(record)

# Tạo và gán dữ liệu vào AgGrid hiện dữ liệu lên bảng
record = dta.sheet1.get_all_records()
df = pd.DataFrame(record)

if record:
# if record: tương đương với if  len(record) > 0:
    loc = df[
        (df["Zone"]==zone)
        &
        (df["Ben"]== trai_phai)
        &
        (df["May"]==may)
        &
        (df["MaHang"]== ma_hang)
    ]
if trai_phai == "T":
    ben = "bên trái"
else:
    ben = "bên phải"
gb = GridOptionsBuilder.from_dataframe(loc)
# chỉ cho phép người dùng chọn duy nhất một dòng
gb.configure_selection("single")
# cầu hình các tùy chọn hiện ẩn các cột theo ý muốn
gb.configure_column("ID", hide=True)
gb.configure_column("Zone", hide=True)
gb.configure_column("May", hide=True)
gb.configure_column("MaHang", hide=True)
gb.configure_column("Ben", hide=True)

# Đổi tên tiêu đề cột khi hiển thị
gb.configure_column("TenKhuon", header_name=f"Tên khuôn {ben}",)
gb.configure_column("TrongLuong", header_name=f"Số nhựa {ben}")

# đóng gói những tùy chọn trên vào biến "tuy_chon_hien_thi"
tuy_chon_hien_thi = gb.build()
st.write(f"Số nhựa: {zone} | {may} |  {ma_hang} | {ben}")
bang = AgGrid(loc,gridOptions=tuy_chon_hien_thi)
selected = bang.get("selected_rows")

# hàm sửa số nhựa__________________________
def sua_so_nhua():
    record = dta.sheet1.get_all_records()
    df = pd.DataFrame(record)
    id_sua = st.session_state["id"]

    if id_sua is None:
        st.toast("⚠️ Vui lòng chọn một dòng trên bảng số nhựa trước khi sửa.")
        #st.stop()
        return
    elif sua_nhua is None:
        st.toast("⚠️ Vui lòng nhập số nhựa cần sửa.")
        #st.stop()
        return
    dong = df[df["ID"] == id_sua].index[0]
    dong_sheet = dong + 2
    dta.sheet1.update_cell(dong_sheet, 7, sua_nhua)
    st.toast(
        f"✅ Bạn vừa sửa lại số nhựa khuôn {st.session_state['tenkhuon']} "
        f"bên {benkhuon} "
        f"mã {st.session_state['mahang']}, "
        f"{st.session_state['may']}, "
        f"{st.session_state['zone']}"
    )
#--------------------------------

if selected is not None and not selected.empty:
    row = selected.iloc[0]
    st.session_state["id"] = row["ID"]
    st.session_state["zone"] = row["Zone"]
    st.session_state["may"] = row["May"]
    st.session_state["mahang"] = row["MaHang"]
    st.session_state["trai_phai"] = row["Ben"]
    st.session_state["tenkhuon"] = row["TenKhuon"]
    st.session_state["nhua"] = float(row["TrongLuong"])
with st.expander("✏️ Sửa / Xóa khuôn"):
    if trai_phai == "T":
        benkhuon = "Trái"
    else:
        benkhuon = "Phải"
    #st.write(f"➕ Sửa lại số nhựa khuôn {st.session_state['tenkhuon']} bên {benkhuon} mã {st.session_state['mahang']}, {st.session_state['may']},  {st.session_state['zone']}")
    st.write(
        f"➕ Sửa lại số nhựa khuôn {st.session_state['tenkhuon']} "
        f"bên {benkhuon} "
        f"mã {st.session_state['mahang']}, "
        f"{st.session_state['may']}, "
        f"{st.session_state['zone']}"
    )
    st.write("➕ Nếu bạn muốn sửa lại số nhựa thì nhập số nhựa mới vào ô bên dưới rồi bấm nút Sửa")

    sua_nhua = st.number_input(
        "📋 Nhập số nhựa sửa",
        min_value=1.0, max_value=900.0,
        value=None
    )
    col1, col2, col3 = st.columns([1, 1, 8])

    with col1:

    #---------------------
    # thêm mục nhập mã hàng vào đây
    #---------------------

        #nut_sua = st.button("✏️ Sửa", use_container_width=True)

        if st.button("✏️ Sửa", use_container_width=True):
            sua_so_nhua()
    with col2:
        nut_xoa = st.button("🗑 Xóa", use_container_width=True)
        if nut_xoa:
            record = dta.sheet1.get_all_records()
            df = pd.DataFrame(record)
            id_sua = st.session_state["id"]
            if id_sua is None:
                st.toast("⚠️ Vui lòng chọn một dòng trên bảng số nhựa trước khi xóa.")
                st.stop()
            dong = df[df["ID"] == id_sua].index[0]
            dong_sheet = dong + 2
            dta.sheet1.delete_rows(dong_sheet)
            st.toast(
                f"✅ Bạn đã xóa {st.session_state['tenkhuon']} "
                f"bên {benkhuon} "
                f"mã {st.session_state['mahang']}, "
                f"{st.session_state['may']}, "
                f"{st.session_state['zone']}"
            )



