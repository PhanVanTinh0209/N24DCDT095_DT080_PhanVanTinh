"""Mô phỏng Prim DT080. Chạy bằng python mo_phong.py."""
import math
import tkinter as tk
from tkinter import ttk, messagebox

from src.prim import prim, tao_danh_sach_ke
from giai_thich import ly_do

NAVY, INK, MUTED = "#18354a", "#183343", "#526c7b"
GREEN, BLUE, ORANGE = "#127455", "#155dba", "#b04a12"
PAPER, LINE = "#f5f8fb", "#afbfca"
MAU = {
    "Ví dụ 1": (3, [(1,2,4), (1,3,1), (2,3,2)]),
    "Hòa trọng số": (3, [(1,2,1), (1,3,1), (2,3,1)]),
    "Không liên thông": (4, [(1,2,1), (3,4,2)]),
    "Trọng số 0": (3, [(1,2,0), (1,3,5), (2,3,0)]),
    "Đồ thị sáu đỉnh": (6, [(1,2,6), (1,3,2), (2,3,3), (2,4,5),
                               (3,4,1), (3,5,4), (4,5,3), (4,6,7), (5,6,2)])
}


class Bang:
    def __init__(self, parent, columns):
        # Mỗi bảng có thanh cuộn riêng cho các đồ thị nhiều cạnh.
        self.frame = ttk.Frame(parent)
        self.table = ttk.Treeview(self.frame, columns=columns, show="headings", height=4)
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=66, minwidth=38, anchor="center")
        scroll = ttk.Scrollbar(self.frame, command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.table.pack(fill="both", expand=True)
        self.table.tag_configure("first", foreground=BLUE, background="#e6f1ff")

    def fill(self, rows, first=False):
        self.table.delete(*self.table.get_children())
        for i, row in enumerate(rows):
            self.table.insert("", "end", values=row, tags=("first",) if first and not i else ())


class MoPhong:
    def __init__(self, root):
        self.root = root
        self.timer = None
        root.title("DT080 · Mô phỏng Prim")
        width = min(1140, root.winfo_screenwidth()-40)
        height = min(730, root.winfo_screenheight()-100)
        root.geometry(f"{width}x{height}")
        root.minsize(min(780,width), min(480,height))
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI",10), padding=(8,4))
        style.configure("Next.TButton", background=BLUE, foreground="white")
        style.map("Next.TButton", background=[("active","#144d92")])
        style.configure("Treeview", rowheight=26, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", background="#e8eff5", foreground=INK)
        header = tk.Frame(root,bg=NAVY,padx=16,pady=8)
        header.pack(fill="x")
        tk.Label(header,text="Thuật toán Prim",bg=NAVY,fg="white",font=("Segoe UI",16,"bold")).pack(side="left")
        self.stats = tk.Label(header,bg=NAVY,fg="#c6edf2",font=("Segoe UI",11,"bold"))
        self.stats.pack(side="right")

        bar = ttk.Frame(root,padding=(12,6))
        bar.pack(fill="x")
        self.name = tk.StringVar(value="Ví dụ 1")
        presets = ttk.Combobox(bar,values=list(MAU),textvariable=self.name,state="readonly",width=19)
        presets.pack(side="left")
        presets.bind("<<ComboboxSelected>>",self.preset)
        ttk.Button(bar,text="Sửa đồ thị…",command=self.editor).pack(side="left",padx=4)
        self.compact = tk.BooleanVar()
        ttk.Checkbutton(bar,text="Chỉ hiện cây và cạnh đang xét",variable=self.compact,command=self.draw).pack(side="left")
        # Thanh điều khiển nằm trên vùng co giãn của đồ thị.
        nav = ttk.Frame(root,padding=(12,2,12,6))
        nav.pack(fill="x")
        for label, cmd in [("Làm lại",lambda:self.goto(0)),("‹  Trước",lambda:self.goto(self.i-1)),
                           ("Tiếp  ›",lambda:self.goto(self.i+1)),("Chạy",self.play),("Tạm dừng",self.stop)]:
            ttk.Button(nav,text=label,command=cmd,width=9,style="Next.TButton" if label.startswith("Tiếp") else "TButton").pack(side="left",padx=(0,4))
        self.step_label=ttk.Label(nav,font=("Segoe UI",10,"bold"))
        self.step_label.pack(side="right")
        self.progress=ttk.Progressbar(root,mode="determinate")
        self.progress.pack(fill="x")

        body=ttk.Frame(root)
        body.pack(fill="both",expand=True)
        body.columnconfigure(0,weight=3,uniform="body")
        body.columnconfigure(1,weight=2,uniform="body")
        body.rowconfigure(0,weight=1)
        left=tk.Frame(body,bg=PAPER)
        left.grid(row=0,column=0,sticky="nsew")
        self.graph_title=tk.Label(left,bg=PAPER,fg=INK,font=("Segoe UI",13,"bold"),anchor="w",padx=14,pady=5)
        self.graph_title.pack(fill="x")
        legend=tk.Frame(left,bg=PAPER)
        legend.pack(side="bottom",fill="x")
        for label,color in [("━ Trong cây",GREEN),("━━ Vừa chọn",BLUE),("┄ Bỏ qua",ORANGE)]:
            tk.Label(legend,text=label,bg=PAPER,fg=color,padx=5,pady=5).pack(side="left")
        self.canvas=tk.Canvas(left,bg=PAPER,highlightthickness=0,width=1,height=1)
        self.canvas.pack(fill="both",expand=True)
        self.canvas.bind("<Configure>",lambda _:self.draw())
        side=tk.Frame(body,bg="white",padx=12,pady=8)
        side.grid(row=0,column=1,sticky="nsew")
        self.action=tk.Label(side,bg="white",fg=BLUE,font=("Segoe UI",14,"bold"),anchor="w")
        self.action.pack(fill="x")
        self.reason=tk.Label(side,bg="white",fg=INK,font=("Segoe UI",11),anchor="w",justify="left",wraplength=340)
        self.reason.pack(fill="x",pady=(4,6))
        self.delta=tk.Label(side,bg="#edf4f8",fg=INK,anchor="w",justify="left",padx=8,pady=6,wraplength=340)
        self.delta.pack(fill="x",pady=(0,6))
        side.bind("<Configure>",lambda e:[label.configure(wraplength=max(160,e.width-36)) for label in (self.reason,self.delta)])
        self.tabs=ttk.Notebook(side)
        self.tabs.pack(fill="both",expand=True)
        columns=("Trọng số","Đỉnh mới","Cha")
        self.after=Bang(self.tabs,columns)
        self.before=Bang(self.tabs,columns)
        self.tree=Bang(self.tabs,("Cha","Đỉnh","Trọng số"))
        for tab,title in [(self.after,"Heap sau"),(self.before,"Heap trước"),(self.tree,"Cạnh cây")]:
            self.tabs.add(tab.frame,text=title)
        self.root.protocol("WM_DELETE_WINDOW",self.close)
        self.preset()

    def preset(self,event=None):
        n,edges=MAU[self.name.get()]
        self.load(n,edges,1)

    def load(self,n,edges,source):
        steps=[]
        result=prim(tao_danh_sach_ke(n,edges),source,ghi_buoc=lambda *s:steps.append(s))
        self.n,self.edges,self.source=n,edges,source
        self.steps,self.result=steps,result
        self.goto(0)

    def editor(self):
        self.stop()
        win=tk.Toplevel(self.root)
        win.title("Dữ liệu đồ thị")
        win.transient(self.root)
        win.grab_set()
        panel=ttk.Frame(win,padding=12)
        panel.pack(fill="both",expand=True)
        n,s=tk.StringVar(value=self.n),tk.StringVar(value=self.source)
        for label,var in [("Số đỉnh (1–30)",n),("Đỉnh bắt đầu",s)]:
            ttk.Label(panel,text=label).pack(anchor="w")
            ttk.Entry(panel,textvariable=var).pack(fill="x")
        ttk.Label(panel,text="Mỗi dòng là một cạnh: u v trọng_số").pack(anchor="w",pady=(8,2))
        entry=tk.Text(panel,width=38,height=9)
        entry.pack(fill="both",expand=True)
        entry.insert("1.0","\n".join(" ".join(map(str,edge)) for edge in self.edges))
        def apply():
            try:
                edges=[tuple(map(int,row.split())) for row in entry.get("1.0","end").splitlines() if row.strip()]
                self.load(int(n.get()),edges,int(s.get()))
            except ValueError as exc:
                messagebox.showerror("Kiểm tra dữ liệu",str(exc),parent=win)
                return
            self.name.set("Tùy chỉnh")
            win.destroy()
        ttk.Button(panel,text="Nạp đồ thị",command=apply).pack(pady=(8,0))

    def stop(self):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer=None

    def close(self):
        self.stop()
        self.root.destroy()

    def play(self):
        self.stop()
        if self.i<len(self.steps)-1:
            self.goto(self.i+1)
            if self.i<len(self.steps)-1:
                self.timer=self.root.after(1100,self.play)

    def goto(self,index):
        self.stop()
        self.i=max(0,min(index,len(self.steps)-1))
        action,item,heap,nodes,tree,total=self.steps[self.i]
        before=self.steps[self.i-1][2] if self.i else ()
        last=self.i==len(self.steps)-1
        title=action
        if item and item[2]:
            title=f"{'Bỏ qua' if action=='Bỏ qua' else 'Chọn cạnh'} {item[2]} – {item[1]}"
        self.action.configure(text=title,fg=ORANGE if action=="Bỏ qua" else BLUE)
        reason=ly_do(item,before,action=="Bỏ qua")
        if last:
            reason+=("  Hoàn tất. Tổng trọng số MST = "+str(total) if self.result is not None
                     else f"  KHÔNG LIÊN THÔNG. Heap rỗng, còn {self.n-len(nodes)} đỉnh chưa tới được.")
        self.reason.configure(text=reason)
        self.stats.configure(text=f"Đã nhận  {len(nodes)}/{self.n}     ·     Tổng  {total}")
        self.step_label.configure(text=f"Bước {self.i} / {len(self.steps)-1}")
        self.progress.configure(maximum=len(self.steps)-1,value=self.i)
        added=sorted(set(heap)-set(before))
        preview=", ".join(map(str,added[:3])) or "—"
        if len(added)>3: preview+=f"  (+{len(added)-3})"
        self.delta.configure(text=f"Đỉnh trong cây: {', '.join(map(str,nodes)) or '∅'}\nVừa thêm vào heap: {preview}")
        for tab,rows,title in [(self.after,heap,"Heap sau"),(self.before,before,"Heap trước"),(self.tree,tree,"Cạnh cây")]:
            tab.fill(rows,first=tab is not self.tree)
            self.tabs.tab(tab.frame,text=f"{title} ({len(rows)})")
        self.graph_title.configure(text=f"Đồ thị {self.n} đỉnh · {len(self.edges)} cạnh · nguồn {self.source}")
        self.draw()

    def draw(self):
        if not hasattr(self,"steps"): return
        c=self.canvas
        c.delete("all")
        width,height=c.winfo_width(),c.winfo_height()
        if min(width,height)<50: return
        action,item,heap,nodes,tree,total=self.steps[self.i]
        radius=min(width*.39,height*.36,165 if self.n<=4 else 255)
        pos={v:(width/2+radius*math.sin(2*math.pi*(v-1)/self.n),
                height/2-radius*math.cos(2*math.pi*(v-1)/self.n)) for v in range(1,self.n+1)}
        if self.n==1: pos[1]=(width/2,height/2)
        chosen={frozenset((u,v)) for u,v,w in tree}
        current=frozenset(item[1:]) if item and item[2] else None
        labels=[]
        for u,v,w in sorted(self.edges,key=lambda e:(frozenset(e[:2])==current,frozenset(e[:2]) in chosen)):
            pair=frozenset((u,v))
            active=pair==current
            if self.compact.get() and not active and pair not in chosen: continue
            x,y=pos[u]
            X,Y=pos[v]
            color=(ORANGE if action=="Bỏ qua" else BLUE) if active else GREEN if pair in chosen else LINE
            c.create_line(x,y,X,Y,fill=color,width=5 if active else 3 if pair in chosen else 2,dash=(7,4) if active and action=="Bỏ qua" else ())
            if len(self.edges)<=40 or active or pair in chosen:
                labels.append((x*.55+X*.45,y*.55+Y*.45,w,color))
        for x,y,w,color in labels:
            r=10+3*(len(str(w))-1)
            c.create_oval(x-r,y-11,x+r,y+11,fill="white",outline=color)
            c.create_text(x,y,text=w,fill=INK,font=("Segoe UI",9,"bold"))
        for v,(x,y) in pos.items():
            r=18 if self.n<=12 else 11
            if v==(item[1] if item else self.source):
                c.create_oval(x-r-5,y-r-5,x+r+5,y+r+5,outline=ORANGE if action=="Bỏ qua" else BLUE,width=2)
            c.create_oval(x-r,y-r,x+r,y+r,fill=GREEN if v in nodes else NAVY,outline="white",width=2)
            c.create_text(x,y,text=v,fill="white",font=("Segoe UI",10,"bold"))


if __name__=="__main__":
    root=tk.Tk()
    MoPhong(root)
    root.mainloop()
