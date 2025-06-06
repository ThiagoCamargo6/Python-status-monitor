import customtkinter
import threading
import requests
import time
import webbrowser
import json
from datetime import datetime

import ctypes 

myappid = 'mycompany.statusmonitor.v1.2' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÃO INICIAL DA JANELA ---
        self.title("StatusMonitor v1.2 ✨")
        self.geometry("600x400")
        self.resizable(False, False)

        # --- CARREGAR DADOS ---
        self.config = self.carregar_config()
        self.services = self.config.get("services", [])
        self.widgets_services = {}
        
        try:
            self.iconbitmap("assets/icon.ico")
        except Exception:
            print("Aviso: 'assets/app_icon.ico' não encontrado. O ícone padrão será usado.")

        self.criar_widgets()

        self.after(1000, self.ciclo_de_verificacao)

    def carregar_config(self):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar 'config.json': {e}")
            return {"settings": {"refresh_interval_seconds": 60}, "services": []}

    def criar_widgets(self):
        scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Serviços Monitorados")
        scrollable_frame.pack(pady=10, padx=15, fill="both", expand=True)

        for service in self.services:
            nome = service.get("name")
            url = service.get("url")
            
            frame_servico = customtkinter.CTkFrame(scrollable_frame, cursor="hand2")
            frame_servico.pack(pady=5, padx=5, fill="x", expand=True)
            frame_servico.grid_columnconfigure(1, weight=1)
            frame_servico.bind("<Button-1>", lambda e, u=url: self.abrir_url(u))

            icon_label = customtkinter.CTkLabel(frame_servico, text="🌐", font=customtkinter.CTkFont(size=24))
            icon_label.grid(row=0, column=0, rowspan=2, padx=10)
            icon_label.bind("<Button-1>", lambda e, u=url: self.abrir_url(u))
            
            label_nome = customtkinter.CTkLabel(frame_servico, text=nome, font=customtkinter.CTkFont(size=15, weight="bold"), anchor="w")
            label_nome.grid(row=0, column=1, sticky="ew", padx=5)
            label_nome.bind("<Button-1>", lambda e, u=url: self.abrir_url(u))
            
            info_frame = customtkinter.CTkFrame(frame_servico, fg_color="transparent")
            info_frame.grid(row=1, column=1, sticky="ew", padx=5)
            
            icon_latencia = customtkinter.CTkLabel(info_frame, text="⏱️", font=customtkinter.CTkFont(size=16))
            icon_latencia.pack(side="left", padx=(0, 5))
            
            label_latencia = customtkinter.CTkLabel(info_frame, text="- ms", font=customtkinter.CTkFont(size=12), text_color="gray60")
            label_latencia.pack(side="left")
            
            label_timestamp = customtkinter.CTkLabel(info_frame, text="", font=customtkinter.CTkFont(size=12), text_color="gray60")
            label_timestamp.pack(side="left", padx=20)

            status_frame = customtkinter.CTkFrame(frame_servico, fg_color="transparent")
            status_frame.grid(row=0, column=2, rowspan=2, padx=10)
            
            label_status = customtkinter.CTkLabel(status_frame, text="...", font=customtkinter.CTkFont(size=14, weight="bold"), width=80)
            label_status.pack()
            
            bolinha_status = customtkinter.CTkFrame(status_frame, width=80, height=5, corner_radius=3, fg_color="gray")
            bolinha_status.pack(pady=5)
            
            self.widgets_services[nome] = {
                "status": label_status, "bolinha": bolinha_status,
                "latencia": label_latencia, "timestamp": label_timestamp
            }

        self.botao_recarregar = customtkinter.CTkButton(self, text="Recarregar Status", command=self.iniciar_verificacoes)
        self.botao_recarregar.pack(pady=10, padx=15, fill="x")

    def ciclo_de_verificacao(self):
        self.iniciar_verificacoes()
        refresh_ms = self.config["settings"]["refresh_interval_seconds"] * 1000
        self.after(refresh_ms, self.ciclo_de_verificacao)

    def iniciar_verificacoes(self):
        self.botao_recarregar.configure(state="disabled", text="Verificando...")
        threading.Thread(target=self._run_checks_and_reenable_button, daemon=True).start()

    def _run_checks_and_reenable_button(self):
        threads = []
        for service in self.services:
            thread = threading.Thread(target=self.checar_status, args=(service["name"], service["url"]), daemon=True)
            threads.append(thread)
            thread.start()
        for t in threads:
            t.join()
        self.after(0, lambda: self.botao_recarregar.configure(state="normal", text="Recarregar Status"))

    def checar_status(self, nome, url):
        widgets = self.widgets_services[nome]
        status_text, status_color, latencia_text = "...", "gray", "- ms"
        try:
            start_time = time.time()
            resposta = requests.get(url, timeout=10)
            latencia_ms = (time.time() - start_time) * 1000
            if resposta.status_code == 200:
                status_text, status_color = "UP", "#2ECC71"
            else:
                status_text, status_color = f"DOWN ({resposta.status_code})", "#E74C3C"
            latencia_text = f"{latencia_ms:.0f} ms"
        except requests.exceptions.ConnectionError:
            status_text, status_color = "OFFLINE", "#95A5A6"
        except requests.exceptions.Timeout:
            status_text, status_color = "TIMEOUT", "#E67E22"
        except Exception:
            status_text, status_color = "ERRO", "#E74C3C"
        hora_atual = datetime.now().strftime("%H:%M:%S")
        def update_ui():
            widgets["status"].configure(text=status_text, text_color=status_color)
            widgets["bolinha"].configure(fg_color=status_color)
            widgets["latencia"].configure(text=latencia_text)
            widgets["timestamp"].configure(text=f"Às {hora_atual}")
        self.after(0, update_ui)

    def abrir_url(self, url):
        webbrowser.open_new_tab(url)


# --- INICIAR A APLICAÇÃO ---
if __name__ == "__main__":
    app = App()
    app.mainloop()