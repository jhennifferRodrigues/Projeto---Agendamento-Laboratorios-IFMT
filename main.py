# =============================================================================
# SISTEMA DE AGENDAMENTO DE LABORATÓRIOS DE INFORMÁTICA - IFMT
# Instituto Federal de Mato Grosso
#
# Tecnologias utilizadas:
#   - TKINTER: biblioteca padrão do Python para interfaces gráficas
#   - DATETIME: módulo para manipulação de datas e horas
#
# Estruturas de dados utilizadas:
#   - LISTA  : agendamentos = []
#   - TUPLA  : horarios = ("07:00-09:00", ...)
#   - DICIONÁRIO: {"laboratorio": "...", "professor": "...", ...}
# =============================================================================

# ── TKINTER: importação da biblioteca de interface gráfica ──
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont

# ── DATETIME: importação do módulo para trabalhar com datas ──
from datetime import datetime

# =============================================================================
# PALETA DE CORES OFICIAL DO IFMT
# =============================================================================
VERDE_PRINCIPAL  = "#198754"
VERDE_ESCURO     = "#146C43"
VERDE_SIDEBAR    = "#0F6B3D"
VERDE_CLARO      = "#D1E7DD"
VERMELHO         = "#C62828"
CINZA_FUNDO      = "#F5F7F8"
CINZA_BORDA      = "#DDE2E5"
BRANCO           = "#FFFFFF"
TEXTO_ESCURO     = "#212529"
TEXTO_SECUNDARIO = "#6C757D"
LARANJA_BG       = "#FFF3CD"
LARANJA_TEXT     = "#B45309"

# =============================================================================
# USUÁRIO LOGADO
# =============================================================================
CURRENT_USER = "Prof. Carlos Silva"

# =============================================================================
# ESTRUTURAS DE DADOS
# =============================================================================

# ── TUPLA: horários fixos disponíveis (imutável, não pode ser alterado) ──
horarios = ("19:00-19:50", "19:50-20:40", "20:50-21:40", "21:40-22:30")

# Laboratórios disponíveis (tupla, pois são fixos)
laboratorios = (
    "Lab 01 - Informática",
    "Lab 02",
    "Lab 03",
    "Lab 04",
    "Lab 05",
)

# ── LISTA: armazena os agendamentos como dicionários (mutável, cresce dinamicamente) ──
agendamentos = [
    # ── DICIONÁRIO: cada agendamento é representado como um dicionário ──
    {
        "id": 1,
        "laboratorio": "Lab 01 - Informática",
        "professor": "Prof. João Silva",
        "data": "20/06/2026",
        "horario": "19:00-19:50",
        "finalidade": "Aula de Python",
        "status": "Confirmado",
    },
    {
        "id": 2,
        "laboratorio": "Lab 02",
        "professor": "Profa. Maria Santos",
        "data": "21/06/2026",
        "horario": "19:50-20:40",
        "finalidade": "Aula de Redes",
        "status": "Pendente",
    },
    {
        "id": 3,
        "laboratorio": "Lab 03",
        "professor": "Prof. Pedro Costa",
        "data": "22/06/2026",
        "horario": "20:50-21:40",
        "finalidade": "Prática de Circuitos",
        "status": "Confirmado",
    },
    {
        "id": 4,
        "laboratorio": "Lab 01 - Informática",
        "professor": "Profa. Ana Lima",
        "data": "23/06/2026",
        "horario": "21:40-22:30",
        "finalidade": "Projeto Final",
        "status": "Pendente",
    },
    {
        "id": 5,
        "laboratorio": "Lab 04",
        "professor": "Prof. Carlos Mendes",
        "data": "24/06/2026",
        "horario": "19:00-19:50",
        "finalidade": "Experimentos de Óptica",
        "status": "Confirmado",
    },
    {
        "id": 6,
        "laboratorio": "Lab 01 - Informática",
        "professor": "Prof. Carlos Silva",
        "data": "25/06/2026",
        "horario": "20:50-21:40",
        "finalidade": "Aula de Estrutura de Dados",
        "status": "Confirmado",
    },
]

# Contador de IDs (incrementa a cada novo agendamento)
proximo_id = 7


# =============================================================================
# DESENHA O LOGO IFMT (grade de quadrados + círculo)
# =============================================================================
def desenhar_logo_ifmt(parent, bg, tamanho=13, gap=3):
    """
    Desenha o logotipo oficial do IFMT:
      - círculo vermelho no canto superior esquerdo
      - quadrados verdes nos demais nós da grade
    """
    # Células do logo: (linha, coluna, forma)
    celulas = [
        (0, 0, "circle"),   # círculo vermelho
        (0, 1, "square"),
        (0, 2, "square"),
        (1, 0, "square"),
        (1, 1, "square"),
        (2, 0, "square"),
        (2, 1, "square"),
        (2, 2, "square"),
        (3, 0, "square"),
        (3, 1, "square"),
    ]
    cols, rows = 3, 4
    total_w = cols * tamanho + (cols - 1) * gap
    total_h = rows * tamanho + (rows - 1) * gap

    canvas = tk.Canvas(parent, width=total_w, height=total_h,
                       bg=bg, highlightthickness=0)
    canvas.pack(side="left")

    for (r, c, forma) in celulas:
        x1 = c * (tamanho + gap)
        y1 = r * (tamanho + gap)
        x2 = x1 + tamanho
        y2 = y1 + tamanho
        cor = VERMELHO if forma == "circle" else "#2E7D32"
        if forma == "circle":
            canvas.create_oval(x1, y1, x2, y2, fill=cor, outline="")
        else:
            raio = 2
            canvas.create_polygon(
                x1 + raio, y1,
                x2 - raio, y1,
                x2, y1 + raio,
                x2, y2 - raio,
                x2 - raio, y2,
                x1 + raio, y2,
                x1, y2 - raio,
                x1, y1 + raio,
                fill=cor, outline="",
            )
    return canvas


# =============================================================================
# CLASSE PRINCIPAL DA APLICAÇÃO
# =============================================================================
class SistemaAgendamento:
    """
    Classe principal do Sistema de Agendamento de Laboratórios do IFMT.
    ── TKINTER: utiliza tk.Tk() como janela raiz da interface ──
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.pagina_atual = "dashboard"

        # ── TKINTER: configuração da janela principal ──
        self.root.title("Sistema de Agendamento de Laboratórios de Informática - IFMT")
        self.root.geometry("1366x768")
        self.root.configure(bg=VERDE_SIDEBAR)
        self.root.resizable(False, False)

        self._centralizar_janela(1366, 768)
        self._configurar_fontes()
        self._configurar_estilos()
        self._construir_layout()
        self._mostrar_dashboard()

    def _centralizar_janela(self, largura: int, altura: int):
        """Centraliza a janela na tela do usuário."""
        self.data_atual = datetime.now().strftime("%d de %B de %Y")
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - largura) // 2
        y = (sh - altura) // 2
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def _configurar_fontes(self):
        """Configura as fontes do sistema."""
        self.fonte_titulo    = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.fonte_subtitulo = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.fonte_texto     = tkfont.Font(family="Segoe UI", size=10)
        self.fonte_btn       = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.fonte_pequena   = tkfont.Font(family="Segoe UI", size=9)
        self.fonte_numero    = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.fonte_card_lab  = tkfont.Font(family="Segoe UI", size=9)

    def _configurar_estilos(self):
        """Configura estilos ttk (Treeview)."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "IFMT.Treeview",
            background=BRANCO,
            foreground=TEXTO_ESCURO,
            fieldbackground=BRANCO,
            rowheight=32,
            font=("Segoe UI", 10),
        )
        style.configure(
            "IFMT.Treeview.Heading",
            background=VERDE_PRINCIPAL,
            foreground=BRANCO,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        style.map("IFMT.Treeview.Heading", background=[("active", VERDE_ESCURO)])
        style.map("IFMT.Treeview", background=[("selected", VERDE_CLARO)])

    # =========================================================================
    # LAYOUT GERAL
    # =========================================================================
    def _construir_layout(self):
        """Constrói: header full-width no topo, depois sidebar + conteúdo."""

        # ── Frame raiz ──
        self.frame_raiz = tk.Frame(self.root, bg=CINZA_FUNDO)
        self.frame_raiz.pack(fill="both", expand=True)

        # ── Header (largura total) ──
        self._construir_header()

        # ── Linha separadora ──
        tk.Frame(self.frame_raiz, bg=CINZA_BORDA, height=1).pack(fill="x")

        # ── Corpo: sidebar + área de conteúdo ──
        self.frame_corpo = tk.Frame(self.frame_raiz, bg=CINZA_FUNDO)
        self.frame_corpo.pack(fill="both", expand=True)

        self._construir_sidebar()
        self._construir_area_conteudo()

    # =========================================================================
    # HEADER — LARGURA TOTAL
    # =========================================================================
    def _construir_header(self):
        """Cabeçalho branco que cobre toda a largura da janela."""
        header = tk.Frame(self.frame_raiz, bg=BRANCO, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        # ── Esquerda: logo IFMT + textos ──
        frame_esq = tk.Frame(header, bg=BRANCO)
        frame_esq.pack(side="left", padx=20, pady=10)

        # Logo: grade correta do IFMT
        desenhar_logo_ifmt(frame_esq, bg=BRANCO, tamanho=13, gap=3)

        # Texto da instituição
        frame_inst = tk.Frame(frame_esq, bg=BRANCO)
        frame_inst.pack(side="left", padx=(10, 0))
        tk.Label(
            frame_inst, text="Instituto Federal",
            bg=BRANCO, fg=TEXTO_ESCURO,
            font=tkfont.Font(family="Segoe UI", size=11, weight="bold"),
        ).pack(anchor="w")
        tk.Label(
            frame_inst, text="Mato Grosso",
            bg=BRANCO, fg=TEXTO_SECUNDARIO,
            font=tkfont.Font(family="Segoe UI", size=10),
        ).pack(anchor="w")

        # Separador vertical
        tk.Frame(frame_esq, bg=CINZA_BORDA, width=1, height=42).pack(
            side="left", padx=16, pady=4
        )

        # Título do sistema
        tk.Label(
            frame_esq,
            text="Sistema de Agendamento de Laboratórios de Informática",
            bg=BRANCO, fg=VERDE_PRINCIPAL,
            font=tkfont.Font(family="Segoe UI", size=13, weight="bold"),
        ).pack(side="left")

        # ── Direita: data + usuário ──
        frame_dir = tk.Frame(header, bg=BRANCO)
        frame_dir.pack(side="right", padx=20)

        # Avatar + nome do usuário (empacotado primeiro → fica mais à direita)
        frame_usuario = tk.Frame(frame_dir, bg=BRANCO)
        frame_usuario.pack(side="right")

        canvas_av = tk.Canvas(
            frame_usuario, width=36, height=36, bg=BRANCO, highlightthickness=0
        )
        canvas_av.pack(side="left")
        canvas_av.create_oval(2, 2, 34, 34, fill=VERDE_PRINCIPAL, outline="")
        canvas_av.create_text(
            18, 18, text="C",
            fill=BRANCO,
            font=tkfont.Font(family="Segoe UI", size=12, weight="bold"),
        )

        frame_nome = tk.Frame(frame_usuario, bg=BRANCO)
        frame_nome.pack(side="left", padx=(8, 0))
        tk.Label(
            frame_nome, text=CURRENT_USER,
            bg=BRANCO, fg=TEXTO_ESCURO,
            font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
        ).pack(anchor="w")
        tk.Label(
            frame_nome, text="Professor",
            bg=BRANCO, fg=TEXTO_SECUNDARIO,
            font=self.fonte_pequena,
        ).pack(anchor="w")

        # Data atual (empacotada depois → fica à esquerda do usuário)
        # ── DATETIME: exibição da data com datetime.now() ──
        tk.Label(
            frame_dir, text=f"📅  {self.data_atual}",
            bg=BRANCO, fg=TEXTO_ESCURO,
            font=self.fonte_texto,
        ).pack(side="right", padx=(0, 16))

    # =========================================================================
    # SIDEBAR
    # =========================================================================
    def _construir_sidebar(self):
        """Barra lateral verde — sem logo, apenas botões de navegação."""
        self.sidebar = tk.Frame(self.frame_corpo, bg=VERDE_SIDEBAR, width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # ── TKINTER: botões de navegação ──
        self.frame_nav = tk.Frame(self.sidebar, bg=VERDE_SIDEBAR)
        self.frame_nav.pack(fill="both", expand=True, padx=8, pady=10)

        itens_menu = [
            ("dashboard", "🏠", "Dashboard"),
            ("novo",      "➕", "Novo Agendamento"),
        ]

        self.botoes_nav = {}
        for chave, icone, rotulo in itens_menu:
            btn = self._criar_botao_nav(self.frame_nav, icone, rotulo, chave)
            self.botoes_nav[chave] = btn

        # Sair no rodapé
        tk.Frame(self.frame_nav, bg="#0A5C34", height=1).pack(fill="x", pady=8)
        self.botoes_nav["sair"] = self._criar_botao_nav(self.frame_nav, "🚪", "Sair", "sair")

    def _criar_botao_nav(self, parent, icone, rotulo, chave):
        """Cria um botão de navegação na sidebar com hover."""
        frame = tk.Frame(parent, bg=VERDE_SIDEBAR, cursor="hand2", height=50)
        frame.pack(fill="x", pady=2)
        frame.pack_propagate(False)

        conteudo = tk.Frame(frame, bg=VERDE_SIDEBAR, padx=12)
        conteudo.place(relx=0, rely=0, relwidth=1, relheight=1)

        lbl_ic = tk.Label(
            conteudo, text=icone, bg=VERDE_SIDEBAR, fg=BRANCO,
            font=tkfont.Font(family="Segoe UI", size=12),
        )
        lbl_ic.pack(side="left", pady=12)

        lbl_txt = tk.Label(
            conteudo, text=rotulo, bg=VERDE_SIDEBAR, fg=BRANCO,
            font=tkfont.Font(family="Segoe UI", size=11),
        )
        lbl_txt.pack(side="left", padx=(10, 0), pady=12)

        def on_enter(e):
            if self.pagina_atual != chave:
                for w in [frame, conteudo, lbl_ic, lbl_txt]:
                    w.configure(bg=VERDE_PRINCIPAL)

        def on_leave(e):
            if self.pagina_atual != chave:
                for w in [frame, conteudo, lbl_ic, lbl_txt]:
                    w.configure(bg=VERDE_SIDEBAR)

        def on_click(e):
            self._navegar(chave)

        for widget in [frame, conteudo, lbl_ic, lbl_txt]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)

        return {"frame": frame, "conteudo": conteudo, "icone": lbl_ic, "texto": lbl_txt}

    def _atualizar_nav_ativo(self, chave_ativa):
        """Destaca o item de menu ativo."""
        for chave, widgets in self.botoes_nav.items():
            cor = VERDE_PRINCIPAL if chave == chave_ativa else VERDE_SIDEBAR
            for w in widgets.values():
                w.configure(bg=cor)

    # =========================================================================
    # ÁREA DE CONTEÚDO (scrollável)
    # =========================================================================
    def _construir_area_conteudo(self):
        self.area_principal = tk.Frame(self.frame_corpo, bg=CINZA_FUNDO)
        self.area_principal.pack(side="left", fill="both", expand=True)

        self.canvas_scroll = tk.Canvas(
            self.area_principal, bg=CINZA_FUNDO, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            self.area_principal, orient="vertical", command=self.canvas_scroll.yview
        )
        self.canvas_scroll.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.canvas_scroll.pack(side="left", fill="both", expand=True)

        self.frame_conteudo = tk.Frame(self.canvas_scroll, bg=CINZA_FUNDO)
        self.canvas_window = self.canvas_scroll.create_window(
            (0, 0), window=self.frame_conteudo, anchor="nw"
        )
        self.frame_conteudo.bind("<Configure>", self._on_frame_configure)
        self.canvas_scroll.bind("<Configure>", self._on_canvas_configure)
        self.canvas_scroll.bind("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, event):
        self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas_scroll.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas_scroll.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _limpar_conteudo(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
        self.canvas_scroll.yview_moveto(0)

    # =========================================================================
    # NAVEGAÇÃO
    # =========================================================================
    def _navegar(self, chave):
        if chave == "sair":
            if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
                self.root.destroy()
            return

        self.pagina_atual = chave
        self._atualizar_nav_ativo(chave)
        self._limpar_conteudo()

        {
            "dashboard": self._mostrar_dashboard,
            "novo":      self._mostrar_novo_agendamento,
        }.get(chave, self._mostrar_dashboard)()

    # =========================================================================
    # PÁGINA: DASHBOARD
    # =========================================================================
    def _mostrar_dashboard(self):
        """Dashboard: 3 cards indicadores + tabela Todos os Agendamentos."""
        self.pagina_atual = "dashboard"
        self._atualizar_nav_ativo("dashboard")

        pad = tk.Frame(self.frame_conteudo, bg=CINZA_FUNDO)
        pad.pack(fill="both", expand=True, padx=18, pady=16)

        # ── Cards ──
        frame_cards = tk.Frame(pad, bg=CINZA_FUNDO)
        frame_cards.pack(fill="x", pady=(0, 14))

        # ── LISTA: contagem com list comprehension ──
        hoje = datetime.now().strftime("%d/%m/%Y")
        ag_hoje  = len([a for a in agendamentos if a["data"] == hoje])
        pendentes = len([a for a in agendamentos if a["status"] == "Pendente"])

        dados_cards = [
            ("📅", str(ag_hoje).zfill(2),  "Agendamentos\nHoje",         "#E8F5E9", "#2E7D32"),
            ("⏰", str(pendentes).zfill(2), "Pendentes\nde Aprovação",    "#FFF8E1", "#F57F17"),
            ("🧪", "08",                    "Laboratórios\nDisponíveis",  "#FCE4EC", VERMELHO),
        ]

        for icone, numero, label, bg_ic, cor_ic in dados_cards:
            card = tk.Frame(
                frame_cards, bg=BRANCO, bd=1, relief="solid",
                highlightbackground=CINZA_BORDA, highlightthickness=1,
            )
            card.pack(side="left", fill="both", expand=True, padx=5)

            inner = tk.Frame(card, bg=BRANCO, padx=14, pady=14)
            inner.pack(fill="both", expand=True)

            frame_ic = tk.Frame(inner, bg=bg_ic, width=48, height=48)
            frame_ic.pack(side="left")
            frame_ic.pack_propagate(False)
            tk.Label(
                frame_ic, text=icone, bg=bg_ic, fg=cor_ic,
                font=tkfont.Font(family="Segoe UI", size=18),
            ).place(relx=0.5, rely=0.5, anchor="center")

            frame_txt = tk.Frame(inner, bg=BRANCO, padx=10)
            frame_txt.pack(side="left")
            tk.Label(
                frame_txt, text=numero, bg=BRANCO, fg=TEXTO_ESCURO,
                font=self.fonte_numero,
            ).pack(anchor="w")
            tk.Label(
                frame_txt, text=label, bg=BRANCO, fg=TEXTO_SECUNDARIO,
                font=self.fonte_card_lab, justify="left",
            ).pack(anchor="w")

        # ── Tabela: Todos os Agendamentos ──
        card_tab = tk.Frame(
            pad, bg=BRANCO, bd=1, relief="solid",
            highlightbackground=CINZA_BORDA, highlightthickness=1,
        )
        card_tab.pack(fill="both", expand=True)

        # Cabeçalho da seção
        hdr = tk.Frame(card_tab, bg=BRANCO, pady=8)
        hdr.pack(fill="x", padx=14)
        tk.Label(
            hdr, text="Todos os Agendamentos",
            bg=BRANCO, fg=TEXTO_ESCURO,
            font=self.fonte_subtitulo,
        ).pack(side="left")
        tk.Frame(card_tab, bg=CINZA_BORDA, height=1).pack(fill="x")

        # Treeview
        colunas = ("ID", "Laboratório", "Professor", "Data", "Horário", "Finalidade", "Status", "Ações")
        frame_tv = tk.Frame(card_tab, bg=BRANCO)
        frame_tv.pack(fill="both", expand=True)

        self.tabela = ttk.Treeview(
            frame_tv, columns=colunas, show="headings",
            style="IFMT.Treeview", height=12,
        )

        larguras = [35, 150, 155, 85, 105, 180, 90, 80]
        for col, larg in zip(colunas, larguras):
            self.tabela.heading(col, text=col)
            self.tabela.column(
                col, width=larg,
                anchor="center" if col in ("ID", "Ações") else "w",
                minwidth=larg,
            )

        sb = ttk.Scrollbar(frame_tv, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tabela.pack(side="left", fill="both", expand=True)

        self.tabela.tag_configure("confirmado", background="#F0FFF4")
        self.tabela.tag_configure("pendente",   background=LARANJA_BG)

        self._popular_tabela_dashboard()

        # Botões de ação (somente para o usuário logado)
        frame_acoes = tk.Frame(card_tab, bg=BRANCO, pady=10)
        frame_acoes.pack(fill="x", padx=14)

        tk.Button(
            frame_acoes, text="👁  Visualizar",
            bg="#E3F2FD", fg="#1565C0",
            font=self.fonte_btn, relief="flat", cursor="hand2",
            padx=10, pady=4,
            command=self._visualizar_agendamento,
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            frame_acoes, text="✏  Editar",
            bg="#E8F5E9", fg=VERDE_ESCURO,
            font=self.fonte_btn, relief="flat", cursor="hand2",
            padx=10, pady=4,
            command=self._editar_agendamento,
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            frame_acoes, text="🗑  Excluir",
            bg="#FFEBEE", fg=VERMELHO,
            font=self.fonte_btn, relief="flat", cursor="hand2",
            padx=10, pady=4,
            command=self._excluir_agendamento,
        ).pack(side="left")

        tk.Label(
            frame_acoes,
            text="✏ Editar e 🗑 Excluir disponíveis apenas para seus próprios agendamentos.",
            bg=BRANCO, fg=TEXTO_SECUNDARIO,
            font=self.fonte_pequena,
        ).pack(side="right")

    def _popular_tabela_dashboard(self):
        """Preenche a tabela com os dados de agendamentos."""
        for row in self.tabela.get_children():
            self.tabela.delete(row)

        # ── LISTA: iteração sobre a lista de dicionários ──
        for ag in agendamentos:
            acoes = "👁 ✏ 🗑" if ag["professor"] == CURRENT_USER else "👁"
            tag = "confirmado" if ag["status"] == "Confirmado" else "pendente"
            self.tabela.insert(
                "", "end",
                iid=ag["id"],
                values=(
                    ag["id"],
                    ag["laboratorio"],
                    ag["professor"],
                    ag["data"],
                    ag["horario"].replace("-", " - "),
                    ag["finalidade"],
                    ag["status"],
                    acoes,
                ),
                tags=(tag,),
            )

    # =========================================================================
    # AÇÕES DA TABELA
    # =========================================================================
    def _visualizar_agendamento(self):
        """Exibe detalhes do agendamento selecionado."""
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um agendamento na tabela.")
            return

        ag_id = int(selecionado[0])
        ag = next((a for a in agendamentos if a["id"] == ag_id), None)
        if not ag:
            return

        janela = tk.Toplevel(self.root)
        janela.title("Detalhes do Agendamento")
        janela.geometry("460x360")
        janela.configure(bg=BRANCO)
        janela.resizable(False, False)
        janela.grab_set()

        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        janela.geometry(f"460x360+{(sw-460)//2}+{(sh-360)//2}")

        tk.Label(
            janela, text="Detalhes do Agendamento",
            bg=BRANCO, fg=TEXTO_ESCURO, font=self.fonte_subtitulo,
        ).pack(anchor="w", padx=20, pady=(16, 4))
        tk.Frame(janela, bg=CINZA_BORDA, height=1).pack(fill="x", padx=20)

        frame_det = tk.Frame(janela, bg=BRANCO, padx=20, pady=10)
        frame_det.pack(fill="both", expand=True)

        def linha(lbl, val):
            f = tk.Frame(frame_det, bg=BRANCO)
            f.pack(fill="x", pady=4)
            tk.Label(
                f, text=lbl, bg=BRANCO, fg=TEXTO_SECUNDARIO,
                font=tkfont.Font(family="Segoe UI", size=9, weight="bold"),
                width=18, anchor="w",
            ).pack(side="left")
            tk.Label(
                f, text=val, bg=BRANCO, fg=TEXTO_ESCURO, font=self.fonte_texto,
            ).pack(side="left")

        linha("ID:",           str(ag["id"]))
        linha("Laboratório:",  ag["laboratorio"])
        linha("Professor:",    ag["professor"])
        linha("Data:",         ag["data"])
        linha("Horário:",      ag["horario"])
        linha("Status:",       ag["status"])
        linha("Finalidade:",   ag["finalidade"])

        tk.Button(
            janela, text="Fechar",
            bg=VERDE_PRINCIPAL, fg=BRANCO,
            font=self.fonte_btn, relief="flat", cursor="hand2",
            padx=20, pady=6, command=janela.destroy,
        ).pack(pady=14)

    def _editar_agendamento(self):
        """Edita o agendamento selecionado — apenas se for do usuário logado."""
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um agendamento na tabela.")
            return

        ag_id = int(selecionado[0])
        ag = next((a for a in agendamentos if a["id"] == ag_id), None)
        if not ag:
            return

        if ag["professor"] != CURRENT_USER:
            messagebox.showwarning(
                "Sem permissão",
                "Você só pode editar seus próprios agendamentos.",
            )
            return

        janela = tk.Toplevel(self.root)
        janela.title("Editar Agendamento")
        janela.geometry("500x420")
        janela.configure(bg=BRANCO)
        janela.resizable(False, False)
        janela.grab_set()

        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        janela.geometry(f"500x420+{(sw-500)//2}+{(sh-420)//2}")

        tk.Label(
            janela, text="Editar Agendamento",
            bg=BRANCO, fg=TEXTO_ESCURO, font=self.fonte_subtitulo,
        ).pack(anchor="w", padx=20, pady=(16, 4))
        tk.Frame(janela, bg=CINZA_BORDA, height=1).pack(fill="x", padx=20)

        inner = tk.Frame(janela, bg=BRANCO, padx=24, pady=14)
        inner.pack(fill="both", expand=True)

        var_lab  = tk.StringVar(value=ag["laboratorio"])
        var_data = tk.StringVar(value=ag["data"])
        var_hor  = tk.StringVar(value=ag["horario"])

        def campo(txt, widget_fn):
            tk.Label(
                inner, text=txt, bg=BRANCO, fg=TEXTO_ESCURO,
                font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
            ).pack(anchor="w", pady=(8, 2))
            w = widget_fn(inner)
            w.pack(fill="x", ipady=3)

        campo("Laboratório", lambda p: ttk.Combobox(
            p, textvariable=var_lab, values=list(laboratorios), state="readonly",
            font=self.fonte_texto,
        ))
        campo("Data (dd/mm/aaaa)", lambda p: tk.Entry(
            p, textvariable=var_data, font=self.fonte_texto, relief="solid", bd=1,
        ))
        campo("Horário", lambda p: ttk.Combobox(
            p, textvariable=var_hor, values=list(horarios), state="readonly",
            font=self.fonte_texto,
        ))

        tk.Label(inner, text="Finalidade", bg=BRANCO, fg=TEXTO_ESCURO,
                 font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
                 ).pack(anchor="w", pady=(8, 2))
        txt_fin = tk.Text(inner, height=3, font=self.fonte_texto, relief="solid", bd=1)
        txt_fin.insert("1.0", ag["finalidade"])
        txt_fin.pack(fill="x")

        def salvar():
            global agendamentos
            # ── DATETIME: validação da data ──
            try:
                datetime.strptime(var_data.get().strip(), "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Erro", "Data inválida. Use dd/mm/aaaa.")
                return

            # ── LISTA/DICIONÁRIO: atualização do dicionário na lista ──
            for i, a in enumerate(agendamentos):
                if a["id"] == ag_id:
                    agendamentos[i]["laboratorio"] = var_lab.get()
                    agendamentos[i]["data"]         = var_data.get().strip()
                    agendamentos[i]["horario"]       = var_hor.get()
                    agendamentos[i]["finalidade"]    = txt_fin.get("1.0", "end").strip()
                    break

            self._popular_tabela_dashboard()
            messagebox.showinfo("Sucesso", "Agendamento atualizado com sucesso!")
            janela.destroy()

        frame_btns = tk.Frame(inner, bg=BRANCO)
        frame_btns.pack(fill="x", pady=(12, 0))
        tk.Button(
            frame_btns, text="Cancelar",
            bg=BRANCO, fg=TEXTO_ESCURO, font=self.fonte_btn,
            relief="solid", bd=1, cursor="hand2", padx=16, pady=5,
            command=janela.destroy,
        ).pack(side="right", padx=(6, 0))
        tk.Button(
            frame_btns, text="✓  Salvar",
            bg=VERDE_PRINCIPAL, fg=BRANCO, font=self.fonte_btn,
            relief="flat", cursor="hand2", padx=16, pady=5,
            activebackground=VERDE_ESCURO, activeforeground=BRANCO,
            command=salvar,
        ).pack(side="right")

    def _excluir_agendamento(self):
        """Exclui o agendamento selecionado — apenas se for do usuário logado."""
        global agendamentos
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um agendamento na tabela.")
            return

        ag_id = int(selecionado[0])
        ag = next((a for a in agendamentos if a["id"] == ag_id), None)
        if not ag:
            return

        if ag["professor"] != CURRENT_USER:
            messagebox.showwarning(
                "Sem permissão",
                "Você só pode excluir seus próprios agendamentos.",
            )
            return

        if messagebox.askyesno(
            "Confirmar Exclusão",
            f"Excluir '{ag['laboratorio']}' em {ag['data']}?\n\nEsta ação não pode ser desfeita.",
        ):
            # ── LISTA: remoção do dicionário da lista ──
            agendamentos = [a for a in agendamentos if a["id"] != ag_id]
            self._popular_tabela_dashboard()
            messagebox.showinfo("Sucesso", "Agendamento excluído com sucesso!")

    # =========================================================================
    # PÁGINA: NOVO AGENDAMENTO
    # =========================================================================
    def _mostrar_novo_agendamento(self):
        """Formulário para criar novo agendamento."""
        pad = tk.Frame(self.frame_conteudo, bg=CINZA_FUNDO)
        pad.pack(fill="both", expand=True, padx=18, pady=16)

        tk.Label(
            pad, text="Novo Agendamento",
            bg=CINZA_FUNDO, fg=TEXTO_ESCURO, font=self.fonte_titulo,
        ).pack(anchor="w", pady=(0, 14))

        card = tk.Frame(
            pad, bg=BRANCO, bd=1, relief="solid",
            highlightbackground=CINZA_BORDA, highlightthickness=1,
        )
        card.pack(anchor="center", ipadx=10, ipady=10)
        card.configure(width=560)

        inner = tk.Frame(card, bg=BRANCO, padx=24, pady=20)
        inner.pack(fill="both")

        tk.Label(
            inner, text="Preencha os dados para agendar um laboratório",
            bg=BRANCO, fg=TEXTO_SECUNDARIO, font=self.fonte_pequena,
        ).pack(anchor="w", pady=(0, 12))

        var_lab  = tk.StringVar()
        var_data = tk.StringVar()
        var_hor  = tk.StringVar()

        def campo(txt, widget_fn):
            tk.Label(
                inner, text=txt, bg=BRANCO, fg=TEXTO_ESCURO,
                font=tkfont.Font(family="Segoe UI", size=10, weight="bold"), anchor="w",
            ).pack(fill="x", pady=(8, 2))
            w = widget_fn(inner)
            w.pack(fill="x", ipady=4)

        campo("Laboratório", lambda p: ttk.Combobox(
            p, textvariable=var_lab, values=list(laboratorios),
            state="readonly", font=self.fonte_texto, width=60,
        ))

        # Data + Horário na mesma linha
        tk.Label(
            inner, text="Data", bg=BRANCO, fg=TEXTO_ESCURO,
            font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
        ).pack(anchor="w", pady=(8, 2))
        frame_dh = tk.Frame(inner, bg=BRANCO)
        frame_dh.pack(fill="x")
        tk.Entry(
            frame_dh, textvariable=var_data,
            font=self.fonte_texto, relief="solid", bd=1,
        ).pack(side="left", fill="both", expand=True, ipady=4)
        tk.Label(
            frame_dh, text="  Horário  ", bg=BRANCO, fg=TEXTO_ESCURO,
            font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
        ).pack(side="left", padx=(12, 4))
        ttk.Combobox(
            frame_dh, textvariable=var_hor, values=list(horarios),
            state="readonly", font=self.fonte_texto, width=15,
        ).pack(side="left", ipady=3)

        tk.Label(
            inner, text="Finalidade / Observações", bg=BRANCO, fg=TEXTO_ESCURO,
            font=tkfont.Font(family="Segoe UI", size=10, weight="bold"),
        ).pack(anchor="w", pady=(8, 2))
        txt_fin = tk.Text(inner, height=5, font=self.fonte_texto, relief="solid", bd=1, wrap="word")
        txt_fin.pack(fill="x")

        frame_btns = tk.Frame(inner, bg=BRANCO)
        frame_btns.pack(fill="x", pady=(14, 0))

        tk.Button(
            frame_btns, text="Cancelar",
            bg=BRANCO, fg=TEXTO_ESCURO, font=self.fonte_btn,
            relief="solid", bd=1, cursor="hand2", padx=18, pady=6, width=14,
            command=lambda: self._navegar("dashboard"),
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            frame_btns, text="✓  Confirmar Agendamento",
            bg=VERDE_PRINCIPAL, fg=BRANCO, font=self.fonte_btn,
            relief="flat", cursor="hand2", padx=18, pady=6,
            activebackground=VERDE_ESCURO, activeforeground=BRANCO,
            command=lambda: self._salvar_agendamento(
                var_lab.get(), var_data.get(), var_hor.get(),
                txt_fin.get("1.0", "end").strip(),
            ),
        ).pack(side="right")

    # =========================================================================
    # LÓGICA: SALVAR AGENDAMENTO
    # =========================================================================
    def _salvar_agendamento(self, lab, data, horario, finalidade):
        """
        Valida e salva novo agendamento.
        ── DATETIME: valida o formato da data ──
        ── LISTA/DICIONÁRIO: adiciona dicionário à lista ──
        """
        global agendamentos, proximo_id

        if not lab:
            messagebox.showerror("Erro", "Selecione um laboratório.")
            return
        if not data.strip():
            messagebox.showerror("Erro", "Informe a data do agendamento.")
            return
        if not horario:
            messagebox.showerror("Erro", "Selecione um horário.")
            return
        if not finalidade.strip():
            messagebox.showerror("Erro", "Informe a finalidade do agendamento.")
            return

        # ── DATETIME: validação da data ──
        try:
            datetime.strptime(data.strip(), "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro de Data", "Data inválida. Use o formato dd/mm/aaaa.")
            return

        # ── DICIONÁRIO: criação do novo agendamento ──
        novo = {
            "id":          proximo_id,
            "laboratorio": lab,
            "professor":   CURRENT_USER,
            "data":        data.strip(),
            "horario":     horario,
            "finalidade":  finalidade.strip(),
            "status":      "Pendente",
        }

        # ── LISTA: adição à lista de agendamentos ──
        agendamentos.append(novo)
        proximo_id += 1

        messagebox.showinfo(
            "Sucesso",
            "Agendamento realizado com sucesso!\nSeu pedido foi enviado para aprovação.",
        )
        self._navegar("dashboard")


# =============================================================================
# PONTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    # ── TKINTER: criação da janela raiz ──
    root = tk.Tk()
    app = SistemaAgendamento(root)
    # ── TKINTER: loop principal da interface gráfica ──
    root.mainloop()
