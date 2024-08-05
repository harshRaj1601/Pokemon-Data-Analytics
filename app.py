import streamlit as st
import pandas as pd
import plotly.express as px

# UI Configuration

st.set_page_config(
    page_title="Pokemon App",
    page_icon="☠️",
    layout="wide"
)

# load data

@st.cache_data
def load_data():
    return pd.read_csv("Pokemon.csv",index_col="#")

# UI integration

with st.spinner("loading dataset..."):
    df = load_data()
    # st.snow()


st.title("Pokemon Data Analytics")
st.subheader("A simple data app to analyze Pokemon data")

st.sidebar.title("Menu")
choice = st.sidebar.radio("Options", ["View Data","Visualize Data","Column Analysis"])
if choice == "View Data":
    st.header("View Dataset")
    st.dataframe(df)
elif choice == "Visualize Data":
    st.header("Visualization")
    # scol = st.sidebar.radio("Select a column",df.columns)
    # st.write(f"### Visulaizing {scol}")
    # if df[scol].dtype == "object":
    #     total_unique_values = df[scol].nunique()
    #     st.write(f"Total Unique Values: {total_unique_values}")
    # elif df[scol].dtype == "int64":
    #     st.write(f"Min Value: {df[scol].min()}")
    #     st.write(f"Max Value: {df[scol].max()}")
    #     st.write(f"Mean Value: {df[scol].mean()}")

    cat_cols = df.select_dtypes(include="object").columns.tolist()
    num_cols = df.select_dtypes(exclude="object").columns.tolist()
    cat_cols.remove("Name")
    num_cols.remove("Legendary")
    num_cols.remove("Generation")
    cat_cols.append("Generation")
    cat_cols.append("Legendary")

    snum_cols = st.sidebar.selectbox("Select a numeric column", num_cols)
    scat_cols = st.sidebar.selectbox("Select a catagorical column", cat_cols)

    c1, c2 = st.columns(2)

    # visualization

    fig1 = px.histogram(df,x=snum_cols,
                        title=f"Distribution of {snum_cols}")

    fig2 = px.pie(df,names=scat_cols,title=f"Distribution of {scat_cols}",hole=0.3)

    c1.plotly_chart(fig1)
    c2.plotly_chart(fig2)

    fig3 = px.box(df,x=scat_cols, y=snum_cols, title=f"{snum_cols} by {scat_cols}")
    st.plotly_chart(fig3)

    fig4 = px.treemap(
        df,path=["Generation","Type 1"],
        title="Pokemon type Distribution"
    )

    st.plotly_chart(fig4)

elif choice == "Column Analysis":
    columns = df.columns.tolist()
    columns.remove("Name")
    scol = st.sidebar.selectbox("Select a column", columns)
    if df[scol].dtype == "object":
        vc = df[scol].value_counts()
        most_common = vc.idxmax()
        c1, c2 = st.columns([3,1])
        fig5 = px.histogram(df,x=scol,title=f"Distribution of {scol}")
        c1.plotly_chart(fig5)
        c2.subheader("Total Data")
        c2.dataframe(vc,use_container_width=True)
        c2.metric("Most Common", most_common, int(vc[most_common]))

        c1, c2 = st.columns(2)
        fig2 = px.pie(df,names=scol,title=f"Percentage wise of{scol}",hole=.3)
        c1.plotly_chart(fig2)
        fig3 = px.box(df, x=scol,title=f"{scol} by {scol}")
        c2.plotly_chart(fig3)
        fig = px.funnel_area(names=vc.index, values=vc.values,title=f"{scol} Funnel Area", height=600)
        st.plotly_chart(fig, use_container_width=True)

    else:
        tab1 , tab2 = st.tabs(["Univariate","Bivariate"])
        with tab1:
            score = df[scol].describe()
            fig1 = px.histogram(df, x=scol, title=f"Distribution of {scol}")
            fig2 = px.box(df, x=scol, title=f"{scol} by {scol}")
            c1,c2,c3 = st.columns([1,3,3])
            c1.dataframe(score)
            c2.plotly_chart(fig1)
            c3.plotly_chart(fig2)
        with tab2:
            c1, c2 = st.columns(2)
            col2 = c1.selectbox("Select a Column",df.select_dtypes(include="number").columns.tolist())
            color = c2.selectbox(
                "Select a Color", df.select_dtypes(exclude="number").columns.tolist()
            )
            fig3 = px.scatter(df,x=scol,y=col2,color=color,title=f"{scol} vs {col2}",height=600)
            st.plotly_chart(fig3, use_container_width=True)
