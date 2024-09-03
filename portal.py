import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path
import os
import warnings
warnings.filterwarnings('ignore')

current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
css_file = current_dir/'style.css'


st.set_page_config(
    page_title='Dynamic Data Portal',
    page_icon=':chart_with_upwards_trend:'
)
st.title(':red[Data] at Your Fingertips')
st.subheader('💻From Data to Decisions: Elevate Your Business Performance',divider='rainbow')

file = st.file_uploader("Drop your File Here", type=['csv','xlsx'])

if file is not None:
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)
    st.dataframe(data)
    st.info("File is successfuly uploded")

    st.subheader('Basic Information about :red[Dataset] 🗒', divider='rainbow')

    tab1,tab2,tab3,tab4 = st.tabs(['Summary','Top & Bottom Row','Data Types','Columns'])

    with tab1:
        #styled_summary = data.describe().style.background_gradient(cmap='Blues')
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset')
        st.subheader('Statistical Summary')
        st.dataframe(data.describe().style.background_gradient(cmap='Oranges'))
        #st.write(styled_summary)
  

    with tab2:
        st.subheader('Top Rows')
        toprow = st.slider('Number of Rows you Want:', min_value=1, max_value=data.shape[0], key='top')
        #st.dataframe(data.head(toprow))
        styled_df = data.head(toprow).style.background_gradient(cmap='viridis')
        st.write(styled_df)
        #st.write(styled_df.to_html(), unsafe_allow_html=True)


        st.subheader('Bottom Rows')
        botrow = st.slider('Number of Rows you Want:', min_value=1, max_value=data.shape[0], key='bot')
        styled_df = data.head(botrow).style.background_gradient(cmap='viridis')
        st.write(styled_df)

    with tab3:
        st.subheader('Datatypes of Headers')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader('Column Names in :red[Dataset]')
        st.dataframe(list(data.columns))

#For Analysis and  Visualization
    st.subheader('Column Values :blue[Count]⬇',divider="rainbow")
    with st.expander('Value :blue[Count]⬇'):
        col1,col2=st.columns((2))
        with col1:
            column =st.selectbox('Choose column:',options=list(data.columns))
        with col2:
            toprows=st.number_input('Top Rows',min_value=1,step=1)
        count=st.button('count')
        if (count==True):
            result = data [column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Data Visualization📊',divider='rainbow')
            fig = px.bar(data_frame = result,x=column,y='count',text='count')
            st.plotly_chart(fig)

           # fig =px.line(data_frame=result,x=column, y='count',text='count')
            #st.plotly_chart(fig)
    st.subheader('Groupby:Simplify your :red[Data]📚')
    st.write('Groupby lets you summarize data')
    with st.expander('Groupby your column'):
        col1,col2,col3 = st.columns((3))
        with col1:
            groupby_cols = st.multiselect('Choose your column to group',options=list(data.columns))
        with col2:
            operation_col = st.selectbox('Choose column for operation',options=list(data.columns))
        with col3:
            operation_list = st.selectbox('Choose Operation to perform',options=['sum','max','min','mean'])
        if(groupby_cols):
            result=data.groupby(groupby_cols).aggregate(newcol = (operation_col,operation_list)).reset_index()
            st.dataframe(result)

            st.subheader('Data Visualization:bar_chart:')
            graphs = st.selectbox('Choose Graph',options=['line','bar','pie','sunbrust'])

            if (graphs=='line'):
                x_axis =st.selectbox('Choose X axis',options=list(result.columns))
                y_axis=st.selectbox('Choose Y axis',options=list(result.columns))
                color = st.selectbox('Choose Color',options=[None]+list(result.columns))
                fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)
            elif(graphs=='bar'):
                x_axis =st.selectbox('Choose X axis',options=list(result.columns))
                y_axis=st.selectbox('Choose Y axis',options=list(result.columns))
                color = st.selectbox('Choose Color',options=[None]+list(result.columns))
                facet_col=st.selectbox('Col Info',options=[None]+list(result.columns))
                fig = px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
                st.plotly_chart(fig)

            elif(graphs=='pie'):
                values = st.selectbox('Choose number of values',options=list(result.columns))
                names = st.selectbox('Choose Labels',options=list(result.columns))
                fig = px.pie(data_frame=result,values=values,names=names)
                st.plotly_chart(fig)

            elif(graphs=='sunbrust'):
                path = st.multiselect('Choose Path',options=list(result.columns))
                fig = px.sunburst(data_frame=result,path=path,values='newcol')
                st.plotly_chart(fig)




