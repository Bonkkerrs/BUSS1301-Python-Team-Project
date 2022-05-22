import os, sys
sys.path.append(os.path.join(os.getcwd(), 'keywords'))
print(os.getcwd())
from tkinter import *
from correlations.analysis import CorrelationAnalyzer
from keywords.summary import SummaryAcquirer
from keywords.analysis import KeywordsAnalyzer
from comments.category import Category, MovieCategoryAcquirer
from comments.comment import MovieCommentCrawler
from comments.ranking import RankingCrawler
from tkinter.filedialog import askdirectory
from tkinter import ttk



class DoubanManagerApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("豆瓣数据管理大师")
        self.root.resizable(False, False)
        intro_text = ' 欢迎来到豆瓣数据管理大师!\n 请选择功能以进一步分析'
        self.intro = Label(self.root, text=intro_text, font=(10,), foreground='blue',
                           underline=1, anchor='nw', justify=CENTER)
        self.intro.grid(row=0, columnspan=4, column=0, sticky=N)
        self.choice_frame = Frame(self.root)

        self.corr = Button(self.choice_frame, text='相关性分析', command=self.corr_analysis)
        self.wordcloud = Button(self.choice_frame, text='分类TOP短评词云图', command=self.get_wordcloud)
        self.corr1 = Button(self.choice_frame, text='简介关键词分析', command=self.keyword_analysis)
        self.corr.pack(side=LEFT)
        self.wordcloud.pack(side=LEFT)
        self.corr1.pack(side=LEFT)
        self.choice_frame.grid(row=1, columnspan=4, column=0)
        self.root.mainloop()

    def corr_analysis(self):
        self.root.destroy()
        c = CorrelationAnalysisManagerApp()

    def keyword_analysis(self):
        self.root.destroy()
        k = KeywordManagerApp()
    
    def get_wordcloud(self):
        self.root.destroy()
        w = WordCloundManagerApp()


class CorrelationAnalysisManagerApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("年份-时长-评分相关性分析")
        self.root.resizable(False, False)    
        self.category_label = Label(self.root, text='影片类型：', anchor='e')
        self.category_label.grid(row=0, column=0, sticky=E)
        self.category = Entry(self.root, width=8)
        self.category.grid(row=0, column=1, sticky=W)
        self.entry_frame = Frame(self.root)
        self.add_button = Button(self.entry_frame, text='选择类型', command=self.choose_category)
        self.entry_frame.grid(row=0, column=2, columnspan=2, sticky=W)
        self.add_button.pack(side=LEFT)
        self.add_button2 = Button(self.root, text='确定查询', command=self.analyze_corr)
        self.add_button2.grid(row=1, column=2)
        self.choose_y2l = Button(self.root, text='年份-时长', command=self.length_year_corr)
        self.choose_y2l.grid(row=2, column=0)
        self.choose_y2s = Button(self.root, text='年份-评分', command=self.score_year_corr)
        self.choose_y2s.grid(row=2, column=1)
        self.choose_l2s = Button(self.root, text='时长-评分', command=self.length_score_corr)
        self.choose_l2s.grid(row=2, column=2)
        # 子窗口       
        self.window = Toplevel()
        self.window.title('')
        self.selected_category_list_label = Label(self.window, text='电影分类')
        self.selected_category_list_label.pack()
        self.selected_category_list = Listbox(self.window, border=0, width=12, selectmode=SINGLE)
        self.selected_category_list.configure(justify=CENTER)
        self.selected_category_list.pack()
        self.get_category_list()
        
    def choose_category(self):
        cat_idx = self.selected_category_list.curselection()[0]
        self.category.delete(0, END)
        self.category.insert(0, self.cat_list[cat_idx].type_name)
        self.selected_category = self.cat_list[cat_idx]

    def get_category_list(self):
        m = MovieCategoryAcquirer()
        self.cat_list = m.acquire_category()
        for cat in self.cat_list:
            self.selected_category_list.insert(END, cat)
    
    def analyze_corr(self):
        self.s = CorrelationAnalyzer(category_obj=self.selected_category, query_limit=50)
        
    def length_year_corr(self):
        self.s.length_year()      

    def score_year_corr(self):
        self.s.score_year()

    def length_score_corr(self):
        self.s.length_score()


class KeywordManagerApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("简介关键词分析")
        self.root.resizable(False, False)
        self.category_label = Label(self.root, text='影片类型：', anchor='e')
        self.category_label.grid(row=0, column=0, sticky=E)
        self.category = Entry(self.root, width=8)
        self.category.grid(row=0, column=1, sticky=W)
        self.entry_frame = Frame(self.root)
        self.add_button = Button(self.entry_frame, text='选择类型', command=self.choose_category)
        self.entry_frame.grid(row=0, column=2, columnspan=2, sticky=W)
        self.add_button.pack(side=LEFT)
        self.keyword_btn = Button(self.root,text='关键词查询',command=self.keyword_search)
        self.keyword_btn.grid(row=2,column=3)  
        # 子窗口       
        self.window = Toplevel()
        self.window.title('')
        self.selected_category_list_label = Label(self.window, text='电影分类')
        self.selected_category_list_label.pack()
        self.selected_category_list = Listbox(self.window, border=0, width=12, selectmode=SINGLE)
        self.selected_category_list.configure(justify=CENTER)
        self.selected_category_list.pack()
        self.get_category_list()
        
        
    def keyword_search(self):
        s = SummaryAcquirer(category_obj=self.selected_category)
        k = KeywordsAnalyzer(s.get_summary())
        d = k.text_rank()
        print(d)
        
    def choose_category(self):
        cat_idx = self.selected_category_list.curselection()[0]
        self.category.delete(0, END)
        self.category.insert(0, self.cat_list[cat_idx].type_name)
        self.selected_category = self.cat_list[cat_idx]

    def get_category_list(self):
        m = MovieCategoryAcquirer()
        self.cat_list = m.acquire_category()
        for cat in self.cat_list:
            self.selected_category_list.insert(END, cat)


class WordCloundManagerApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("分类TOP短评词云图生成")
        self.root.resizable(False, False)
        # Row0
        self.category_label = Label(self.root, text='影片类型：', anchor='e')
        self.category_label.grid(row=0, column=0, sticky=E)
        self.category = Entry(self.root, width=8)
        self.category.grid(row=0, column=1, sticky=W)
        self.top_num_label = Label(self.root, text='排名范围：')
        self.top_num_label.grid(row=0, column=2, sticky=E)
        self.top_num = Entry(self.root, width=8)
        self.top_num.grid(row=0, column=3, sticky=W)
        # Row1
        self.var1 = IntVar()
        self.save_pic_label = Checkbutton(self.root, text='保存输出', variable=self.var1,
                                          command=self.save_pic, onvalue=1, offvalue=0)
        self.save_pic_label.grid(row=1, column=0, rowspan=1)
        self.query_btn = Button(self.root, text='查询', command=self.new_query)
        self.query_btn.grid(row=1, column=1)
        self.entry_frame = Frame(self.root)
        self.add_button = Button(self.entry_frame, text='选择类型', command=self.choose_category)
        self.delete_button = Button(self.entry_frame, text='生成词云', command=self.get_wordcloud)
        self.entry_frame.grid(row=1, column=2, columnspan=2, sticky=W)
        self.add_button.pack(side=LEFT)
        self.delete_button.pack(side=LEFT)
        # Row2
        self.output_directory_label = Label(self.root, text='输出路径：')
        self.output_directory_label.grid(row=2, column=0, sticky=E)
        self.output_directory = Entry(self.root, width=20, state='disabled')
        self.output_directory.grid(row=2, column=1, sticky=W, columnspan=2)
        self.output_directory_select = Button(text='选择路径', command=self.selectPath, state='disabled')
        self.output_directory_select.grid(row=2, column=3)
        # 子窗口
        self.window = Toplevel()
        self.window.title('')
        self.selected_category_list_label = Label(self.window, text='电影分类')
        self.selected_category_list_label.pack()
        self.selected_category_list = Listbox(self.window, border=0, width=12, selectmode=SINGLE)
        self.selected_category_list.configure(justify=CENTER)
        self.selected_category_list.pack()
        self.get_category_list()

        self.save_fig = False
        self.auto_fillin()
        self.root.mainloop()

    def new_query(self):
        self.window = Toplevel()
        limit = self.top_num.get()
        if int(limit) > 30:
            self.tree = ttk.Treeview(self.window, show="headings", height=30)  # #创建表格对象
        else:
            self.tree = ttk.Treeview(self.window, show="headings", height=limit)
        self.tree["columns"] = ("排名", "片名", "评分", "简介", "演员", "评论数")

        self.tree.column("排名", width=50, anchor=N)
        self.tree.column("片名", width=100)  # #设置列
        self.tree.column("评分", width=50, anchor=N)
        self.tree.column("简介", width=250)
        self.tree.column("演员", width=300)
        self.tree.column("评论数", width=80)
        self.tree.heading("排名", text="排名")
        self.tree.heading("片名", text="片名")
        self.tree.heading("评分", text="评分")
        self.tree.heading("简介", text="简介")
        self.tree.heading("演员", text="演员")
        self.tree.heading("评论数", text="评论数")
        category_obj = self.selected_category
        r = RankingCrawler(category_obj, limit)
        self.movie_list = r.movie_list
        for k, movie in enumerate(r.movie_list):
            rank = movie.rank
            title = movie.title
            score = movie.score
            regions = movie.regions
            types = movie.types
            vote_count = movie.vote_count
            actors = movie.actors
            detail = '/'.join(regions + types)
            values = (rank, title, score, detail, actors, vote_count)
            self.tree.insert("", k, text=values[0], values=values)
        self.tree.pack()

    def selectPath(self):
        path_ = askdirectory()
        self.output_directory.delete(0, END)
        self.output_directory.insert(0, path_)
        self.directory = path_

    def choose_category(self):
        cat_idx = self.selected_category_list.curselection()[0]
        self.category.delete(0, END)
        self.category.insert(0, self.cat_list[cat_idx].type_name)
        self.selected_category = self.cat_list[cat_idx]

    def get_wordcloud(self):
        idx = int(self.tree.selection()[0].strip('I'), 16) - 1
        movie_obj = self.movie_list[idx]
        m = MovieCommentCrawler(id=movie_obj.id, limit=100)
        fig = m.generate_wordcloud()

        if self.var1.get() == 1:
            fname = os.path.join(self.directory, 'wordcloud.png')
            fig.savefig(fname, dpi=600)

    def auto_fillin(self):
        self.selected_category = Category("剧情", "11")
        self.category.insert(END, '剧情')
        self.top_num.insert(END, '20')

    def get_category_list(self):
        m = MovieCategoryAcquirer()
        self.cat_list = m.acquire_category()
        for cat in self.cat_list:
            self.selected_category_list.insert(END, cat)

    def save_pic(self):
        if self.var1.get() == 0:
            self.output_directory.configure(state='disabled')
            self.output_directory_select.configure(state='disabled')
            self.save_fig = False
        else:
            self.output_directory.configure(state='normal')
            self.output_directory_select.configure(state='normal')
            self.save_fig = True


        
if __name__ == '__main__':
    d = DoubanManagerApp()
    # w = WordCloundManagerApp()
