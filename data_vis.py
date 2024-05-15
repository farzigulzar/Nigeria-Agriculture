import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
import bokeh
from bokeh.plotting import figure
import calendar



# data manipulation
def int_month(w):
    
    for i in np.arange(0,w.size,1):
        w[i]=calendar.month_name[w[i]]
    return w

def read_data(data_path):
    data_ = pd.read_csv(data_path)
    country = pd.read_csv("country.csv")
    data_['Date'] = pd.to_datetime(data_['Date'])

    data_['Profit'] = data_['unit_price']*data_['Profit per unit']
    data_ = pd.merge(data_, country, how='inner', left_on='Export Country', right_on='Country')


    data_.to_csv('cleaned_data.csv', header=True, index=None)
    return data_


def put_filters_working(data_):
    query=data_[data_.columns[0]]==data_[data_.columns[0]]
    
    st.sidebar.header("Selection")
    s_= list(pd.unique(data_['Company']))
    s_=["ALL"]+s_
    company = st.sidebar.selectbox(label="Company ",
                            options=s_)
    if (company!='ALL'):
        query = query & (data_['Company']==company)

    s_= list(pd.unique(data_['Product Name']))
    s_=["ALL"]+s_
    prod_ = st.sidebar.selectbox(label="Product ",options=s_)
    if (prod_!='ALL'):
        query = query & (data_['Product Name']==prod_)

    # Export_c
    s_= list(pd.unique(data_['Export Country']))
    s_=["ALL"]+s_
    Export_c = st.sidebar.selectbox(label="Export Country", options=s_)
    if (Export_c!='ALL'):
        query&=(data_['Export Country']==Export_c)

    # Destination_p
    s_= list(pd.unique(data_['Destination Port']))
    s_=["ALL"]+s_
    Destination_p = st.sidebar.selectbox("Destination Port", s_)
    if (Destination_p!='ALL'):
        query&=(data_['Destination Port']==Destination_p)
    st.sidebar.image("https://ocdn.eu/images/pulscms/NmI7MDA_/19b04a0e578936d3c3ce0c984d632fd7.jpg")

    
    linkedin_url = "https://www.linkedin.com/in/akashpal12/"
    st.sidebar.write("Made with:heart:,:green[*Akash Pal*]")
    # st.sidebar.text("")
    st.sidebar.write("[LinkedIn](%s)" % linkedin_url)
    st.sidebar.write("[Github](%s)" % "https://github.com/farzigulzar/Nigeria-Agriculture")
    return company, prod_, Export_c, Destination_p

# # What are the top-selling products?
# data_.groupby(['Product Name']).agg({'Units Sold':'sum', 'Profit':'sum'}).sort_values('Units Sold', ascending=False)
def create_query(dict,data_):
    query=data_[data_.columns[0]]==data_[data_.columns[0]]

    for key in dict.keys():
        if key!="ALL":
            query &= (data_[dict[key]]==key)
    # if (company!='ALL'):
    #     query = query & (data_['Company']==company)
    # if (prod_!='ALL'):
    #     query = query & (data_['Product Name']==prod_)
    # if (Export_c!='ALL'):
    #     query&=(data_['Export Country']==Export_c)
    # if (Destination_p!='ALL'):
    #     query&=(data_['Destination Port']==Destination_p)
    return query


if __name__=="__main__": 
    st.set_page_config(layout="wide")
    data_ = read_data("https://raw.githubusercontent.com/farzigulzar/Nigeria-Agriculture/main/NG%20agric%20exports/nigeria_agricultural_exports.csv")
    st.title("Nigeria Agriculture Report")

    tab1, tab2, tab3, tab4 = st.tabs(["Sales Performance", "Time Series", "Cost Analysis", "Geographic Data"])
    company, product, export, destination = put_filters_working(data_)
    dicti_query = {company:'Company', product:"Product Name", 
             export:"Export Country", destination:"Destination Port"}
    
    # q_ = create_query(dicti_query, data_)
    # data_[q_]

    with tab1:
            expander_ = st.expander("Insights")
            expander_.write('''
                            * It has been observed that Sesame is the top selling product followed by Cocoa with a very small margin\n
                            * The highest sale revenue was accumulated by Nigeria Auro Export Company, however there are product specfic companies 
                                as well like Farmgate
                                which deals in Rubber
                            * Denmark and Italy are one of the largest Importing countries
                        ''')

            h=300   
            # What are the top-selling products?
            c1, c2 = st.columns(2)
            dict_q_ = dicti_query
            dict_q_ = {company:'Company',  export:"Export Country", destination:"Destination Port"}
            tsp_query = create_query(dict_q_, data_)
            w_= data_[tsp_query].groupby(['Product Name']).agg({'Units Sold':'sum', 'Profit':'sum'}).sort_values('Units Sold', ascending=False)
            w_ = w_.reset_index()
            
            fig_tsp = px.bar(w_, x="Units Sold", y="Product Name",
                            hover_data='Profit', orientation='h')
            fig_tsp.update_layout(title="Top Selling Products", width=500, height=h)
            c1.plotly_chart(fig_tsp, theme="streamlit")
            # c2.text("Raw Values")
            # c2.dataframe(w_)


            # Product sales over country
            dict_q_ = {company:'Company', 
                    export:"Export Country", destination:"Destination Port"}
            tsp_query = create_query(dict_q_, data_)
            fig = px.bar(data_[tsp_query], x="Export Country", y="Product Name", color="Product Name")
            fig.update_layout(title="Product Sales", width=580, height=h)
            c2.plotly_chart(fig)


            c1, c2 = st.columns(2)
            # Which company has the highest sales revenue?
            dict_q_ = { product:"Product Name", 
                    export:"Export Country", destination:"Destination Port"}
            tsp_query = create_query(dict_q_, data_)
            
            w_= data_[tsp_query].groupby(['Company']).agg({'Units Sold':'sum', 'Profit':'sum'}).sort_values('Profit', ascending=False)
            w_ = w_.reset_index()
            
            fig_tsp = px.bar(w_, x="Profit", y="Company",
                            hover_data='Units Sold', orientation='h')
            fig_tsp.update_layout(title="Highest Sales revenues", width=500, height=h)
            c1.plotly_chart(fig_tsp, theme="streamlit")
            

            # average revenue per country
            # dicti_query = {company:'Company', product:"Product Name", destination:"Destination Port"}
            
            val_ = 'Profit per unit'
            # st.dataframe(data_[tsp_query])
            # data_[create_query(dicti_query, data_)]
            t_ = data_.groupby(['Export Country', 'Product Name']).agg({val_:'mean'}).reset_index().pivot(index='Export Country', columns='Product Name', values=val_).reset_index()

            fig = go.Figure(go.Bar(x= t_['Export Country'], y=t_[t_.columns[1]], name=  t_.columns[1]))
            for i in np.arange(2, 9,1):
                fig.add_trace(go.Bar(x= t_['Export Country'], y=t_[t_.columns[i]], name=  t_.columns[i]))
            
            fig.update_layout(barmode='stack' , xaxis={'categoryorder':'category ascending'},
                            title = "Average revenue per Country", yaxis={'title':'Avg Revenue'}, width=580 , height=h  )
            c2.plotly_chart(fig)


            #  Is there any correlation between the units sold and the profit generated?

            t_query = create_query(dicti_query, data_)
            fig = px.scatter( data_[t_query], x='Units Sold', y='Profit', opacity=0.65,
                    trendline='ols', trendline_color_override='white'
                )
            fig.update_layout(title="Correlation between Units sold and Profit generated", width=1100)
            
            st.plotly_chart(fig)
    
    
    with tab2:
        # st.text("")
        expander_ = st.expander("Insights")
        expander_.write('''
                            * April-May in general observes less export, might be because of the heat and crop season
                            * Similar dipping trends have been observed around September as crops season
                            * The highest exports are generally seen in Quarter 4
                            * Post Pandemic recovery is still yet to be observed, as the total export in 2023 is still less than 2021. However it still better than 2022.
                    ''')
        query_ts = create_query(dicti_query, data_)
        # data_[query_ts]
        t1_ = data_[query_ts][['Date', 'Units Sold']].groupby(['Date']).agg({"Units Sold":"sum"})
        # t1_
        c1,c2,c3 = st.columns(3)

        # Monthly
        t1_['m']=t1_.index
        t1_['m']=t1_['m'].dt.month
        w_ = t1_.groupby(['m']).agg({"Units Sold":'sum'})
        w_ = w_.reset_index()
        w_['m']=int_month(w_['m'])
        
        fig = go.Figure(data=[go.Line(
            x=w_['m'],
            y=w_['Units Sold'],
            marker_color=pc.qualitative.Light24[12:] # marker color can be a single color value or an iterable
        )])
        fig.update_layout(title="Monthly",width=300)
        c1.plotly_chart(fig)


        # Quarterly
        t1_['m']=t1_.index
        t1_['m']=t1_['m'].dt.quarter
        w_ = t1_.groupby(['m']).agg({"Units Sold":'sum'})
        w_ = w_.reset_index()
        # w_['m']=int_month(w_['m'])
        w_['m'] = "Q"+w_['m'].astype("string")
        
        fig = go.Figure(data=[go.Line(
            x=w_['m'],
            y=w_['Units Sold'],
            marker_color=pc.qualitative.Light24[4:] # marker color can be a single color value or an iterable
        )])
        fig.update_layout(title="Quarterly",width=300)
        c2.plotly_chart(fig)

        # Yearly
        t1_['m']=t1_.index
        t1_['m']=t1_['m'].dt.year
        w_ = t1_.groupby(['m']).agg({"Units Sold":'sum'})
        w_ = w_.reset_index()
        # w_['m']=int_month(w_['m'])
        
        fig = go.Figure(data=[go.Line(
            x=w_['m'],
            y=w_['Units Sold'],
            marker_color=pc.qualitative.Light24[4:] # marker color can be a single color value or an iterable
        )])
        fig.update_layout(title="Yearly", width=300)
        c3.plotly_chart(fig)

        # Line chart for all dates
        t1_['Date']=pd.to_datetime(list(t1_.index), format = "%d/%m/%Y")
        # t1_['m']
        fig=px.line(t1_,x='Date', y='Units Sold' )
        fig.update_layout(width=1000, title="Units Sold")
        st.plotly_chart(fig)

        # Correlation between Date of purchase and profit margin
        fig = px.scatter( data_[query_ts], x='Date', y='Profit per unit', opacity=0.65,
                    trendline='ols', trendline_color_override='white'
                )
        fig.update_layout(title="Correlation between Units sold and Profit generated", width=1100)
        
        st.plotly_chart(fig)
    
    with tab3:
        expander_ = st.expander("Insights")
        expander_.write(
        '''
        * A linear Negative trend is observed with Sesame, Cashew, Plantain.
        * However rest all products have positive trend.
        ''')
        # What is the cost of goods sold (COGS) as a percentage of revenue?
        query_ts = create_query(dicti_query, data_)

        data_['COGS']=data_['Units Sold']*data_['unit_price']
        data_['COGS percentage revenue']=data_['Units Sold']*data_['unit_price']/data_['Profit']

        fig = px.scatter( data_[query_ts], x='Units Sold', y='Profit', opacity=0.65,
                    trendline='ols', trendline_color_override='white', size = 'COGS percentage revenue', color='Product Name'
                )
        fig.update_layout(title="Correlation between Units sold and Profit generated", width=1100)
        
        st.plotly_chart(fig)
        
    
    with tab4:
        
        h=250
        w=540
        # 1	Which destination ports receive the highest volume of exports?
        c1, c2 = st.columns(2)
        dicti_query = {company:'Company', product:"Product Name", 
             export:"Export Country"}
        
        t_ = data_[create_query(dicti_query, data_)].groupby(['Destination Port']).agg({'Units Sold':'sum'}).sort_values(by =['Units Sold'] , ascending=[True]).reset_index()
        fig = px.bar(t_, y='Destination Port' , x='Units Sold', orientation='h')
        fig.update_layout(title='Highest Volume of Exports', width=w, height=h)
        c1.plotly_chart(fig)

        # 2	What are the transportation modes commonly used for export?

        dicti_query = {company:'Company', product:"Product Name", 
             export:"Export Country", destination:"Destination Port"}
        t_ = data_[create_query(dicti_query, data_)].groupby(['Transportation Mode']).agg({'Transportation Mode':'count'})
        t_.columns=['Count']
        t_ = t_.reset_index()

        
        fig = px.bar(t_, y='Transportation Mode' , x='Count', orientation='h')
        fig.update_layout(title='Highest Volume of Exports', width=w, height=h)
        c2.plotly_chart(fig)


        c3, c4=st.columns(2)
        # 3	Rank the destination port by the export value.
        dicti_query = {company:'Company', product:"Product Name", 
             export:"Export Country"}
        
        t_ = data_[create_query(dicti_query, data_)].groupby(['Destination Port']).agg({'Export Value':'sum'}).sort_values(by=['Export Value'], ascending=True).reset_index()
        # t_
        fig = px.bar(t_, y='Destination Port' , x='Export Value', orientation='h')
        fig.update_layout(title='Destination port by Export value', width=w, height=h)
        c3.plotly_chart(fig)
        

        # 4	Show the top export product for each port.
        dicti_query = {company:'Company', 
             export:"Export Country"}
        t_ = data_[create_query(dicti_query, data_)].groupby(['Destination Port', 'Product Name']).agg({'Units Sold':'sum'}).reset_index()

        df=pd.DataFrame(columns=['Destination Port', 'Product Name', 'Units Sold'])
        for p in data_[create_query(dicti_query, data_)]['Destination Port'].unique():
            df = pd.concat([df, t_[t_['Destination Port']==p].sort_values(by=['Units Sold'], ascending=[False]).reset_index().drop(['index'], axis=1).head(1)], ignore_index=True)
        # df
        fig = px.bar(df, x='Destination Port' , y='Units Sold', text = 'Product Name', orientation='v')
        fig.update_traces(textfont_size=20)
        fig.update_layout(title='Top Export for Ports' ,width=w, height=h)
        c4.plotly_chart(fig)
        