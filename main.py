import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
from service.EventService import EventService
from service.RegisterService import RegisterService
from service.UserService import UserService
from service.InviteService import InviteService
from enumeration.Messages import Messages
import random

root = tk.Tk()
root.title("Pesquisa de Eventos")

def init():
    global event_service
    event_service = EventService()

    global register_service
    register_service = RegisterService()
    
    global user_service
    user_service = UserService()

    global invite_service
    invite_service = InviteService()
    
def create_main_window():
    def check_login():
        email = entry_email.get()
        password = entry_password.get()
        
        global user_service        
        login_message = user_service.check_login(email, password)

        if login_message == Messages.LOGIN_ERROR.value:
            display_message("Erro", login_message, True)
        else:
            logged_user = user_service.get_logged_user()
            display_message("Login", login_message, False)
            if logged_user.get_is_organizador() == 1:
                display_message("Organizador", "Bem-vindo organizador!", False)
            else:
                display_message("Participante", "Bem-vindo participante!", False)
            login_frame.destroy()
            select_action()

    login_frame = tk.Frame(root)
    login_frame.pack(side="left", padx=20, pady=20)

    label_email = tk.Label(login_frame, text="email do Usuário:")
    label_email.pack()

    entry_email = tk.Entry(login_frame)
    entry_email.pack()

    label_password = tk.Label(login_frame, text="Senha:")
    label_password.pack()

    entry_password = tk.Entry(login_frame, show="*")
    entry_password.pack()

    button_login = tk.Button(login_frame, text="Entrar", command=check_login)
    button_login.pack(pady=10)

    button_register = tk.Button(login_frame, text="Registrar", command=register_window)
    button_register.pack(pady=10)

    button_close = tk.Button(login_frame, text="Fechar", command=root.destroy)
    button_close.pack(pady=10)

def register_window():
    def save_user():
        email = entry_email.get()
        name = entry_name.get()
        password = entry_password.get()
        password_confirm = entry_confirm_password.get()
        if name == "" or password == "" or email == "":
            display_message("Erro", "Por favor, preencha todos os campos!", True)
            return
        if password != password_confirm:
            display_message("Erro", "As senhas devem ser iguais!", True)
            return
        
        global user_service
        message = user_service.create_user(name, email, password, False)
        
        if message == Messages.USER_INSERT_OK.value:
            display_message("Sucesso", message, False)
            register.destroy()
        else:
            display_message("Erro", message, True)
            entry_email.delete(0, tk.END)

    register = tk.Toplevel(root)
    register.title("Cadastro de Usuário")

    label_email = tk.Label(register, text="email do Usuário:")
    label_email.pack()

    entry_email = tk.Entry(register)
    entry_email.pack()

    label_name = tk.Label(register, text="Nome do Usuário:")
    label_name.pack()

    entry_name = tk.Entry(register)
    entry_name.pack()

    label_password = tk.Label(register, text="Senha:")
    label_password.pack()

    entry_password = tk.Entry(register, show="*")
    entry_password.pack()

    label_confirm_password = tk.Label(register, text="Confirme sua senha:")
    label_confirm_password.pack()

    entry_confirm_password = tk.Entry(register, show="*")
    entry_confirm_password.pack()

    button_register = tk.Button(register, text="Registrar", command=save_user)
    button_register.pack(pady=10)
    
def event_window(event):
    
    if event == None:
        pre_title = tk.StringVar(value = None)
        pre_description = tk.StringVar(value = None)
        pre_date = tk.StringVar(value = None)
        pre_time = tk.StringVar(value = None)
        entry_visibility = tk.StringVar(value = None)
        pre_location = tk.StringVar(value = None)
    else:
        pre_title = tk.StringVar(value = event.get_titulo())
        pre_description = tk.StringVar(value = event.get_descricao())
        pre_date = tk.StringVar(value = event.get_data())
        pre_time = tk.StringVar(value = event.get_horario())
        entry_visibility = tk.StringVar(value = event.get_visibilidade())
        pre_location = tk.StringVar(value = event.get_local())
        
    
    def save_or_update_event(event):
       
        if entry_title.get() == "":
            display_message("Erro", "Por favor, preencha o titulo corretamente!", True)
            return
        
        if entry_date.get() == "":
            display_message("Erro", "A data não pode ser vazia", True)
            return
        
        data_atual = str(datetime.today().date())
        data = entry_date.get_date().strftime("%Y-%m-%d")
             
        if data_atual > data:
            display_message("Erro", "Não é permitido criar um evento para uma data retroativa!", True)
            return
        
        if event == None:
            id = None
        else:
            id = event.get_id()
            
        global event_service
        global user_service        
        message = event_service.create_or_update_event(id, entry_title.get(), entry_description.get(), entry_location.get(), data, entry_time.get(), entry_visibility.get(), user_service.get_logged_user())
        
        if message == Messages.EVENT_INSERT_OR_UPDATE_OK.value:
            display_message("Sucesso", message, False)
            
            if not user_service.get_logged_user().get_is_organizador():
                update_user(user_service.get_logged_user().get_id(), True)
                
            event_window.destroy()
                
        else:
            display_message("Erro", message, True)

    event_window = tk.Toplevel(root)
    event_window.title("Cadastro de Evento")

    label_title = tk.Label(event_window, text="Título do Evento:")
    label_title.pack()

    entry_title = tk.Entry(event_window, textvariable = pre_title)
    entry_title.pack()
    
    label_description = tk.Label(event_window, text="Descrição do Evento:")
    label_description.pack()

    entry_description = tk.Entry(event_window, textvariable = pre_description)
    entry_description.pack()

    label_location = tk.Label(event_window, text="Local:")
    label_location.pack()

    entry_location = tk.Entry(event_window, textvariable = pre_location)
    entry_location.pack()
    
    label_date = tk.Label(event_window, text="Data:")
    label_date.pack()

    entry_date = DateEntry(event_window, width=12, background='darkblue', foreground='white', borderwidth=2, textvariable = pre_date)
    entry_date.pack(padx=10, pady=10)
    
    label_time = tk.Label(event_window, text="Horário:")
    label_time.pack()

    entry_time = tk.Entry(event_window, textvariable = pre_time)
    entry_time.pack()
    
    label_visibility = tk.Label(event_window, text="Visibilidade:")
    label_visibility.pack()
  
    private_rb = ttk.Radiobutton(event_window, text="PRIVADO", variable=entry_visibility, value=1)
    private_rb.pack(pady=10)

    female_rb = ttk.Radiobutton(event_window, text="PÚBLICO", variable=entry_visibility, value=0)
    female_rb.pack(pady=10)    

    button_register = tk.Button(event_window, text="Registrar", command=lambda:save_or_update_event(event))
    button_register.pack(pady=10)

    button_delete = tk.Button(event_window, text="Deletar Evento", command=lambda:delete_event(event, event_window))  
      
    if event != None:
        button_delete.pack(pady=10)
    else: 
        button_delete.forget()

def participants_window(event):
    def set_checkin(user_id, event_id, checkin):
        if checkin == 0:
            register_service.update_checkin(user_id, event_id)
            display_message("Sucesso", "Checkin realizado", False)
            participants_window.destroy()

    participants = event_service.get_registers(event.get_id())

    participants_window = tk.Toplevel(root)
    participants_window.title("Participantes")

    if len(participants) == 0:
        id_label = tk.Label(participants_window, text="Esse evento não possui inscritos")
        id_label.grid(row = 0, column=0, pady=3, sticky="w", padx=5)

    id_label = tk.Label(participants_window, text="ID")
    id_label.grid(row = 0, column=0, pady=3, sticky="w", padx=5)

    checkin_label = tk.Label(participants_window, text="Checkin realizado?") 
    checkin_label.grid(row = 0, column=1, pady=3, sticky="e", padx=5)

    i = 1
    for participant in participants:
        date_event_label = tk.Label(participants_window, text=participant.get_id())
        date_event_label.grid(row = i, column=0, pady=3, sticky="w", padx=5)

        print(participant.get_checkin_timestamp())

        checkin_button = tk.Button(participants_window, text=participant.get_checkin_timestamp() if participant.get_checkin_done() else 'Não', command=lambda:set_checkin(participant.get_id(),event.get_id(), participant.get_checkin_done())) 
        checkin_button.grid(row = i, column=1, pady=3, sticky="e", padx=5)
        i += 1

def show_user_events():    
    def update_event(selected_event):             
        data_atual = str(datetime.today().date())
        data = selected_event.get_data()
             
        if data_atual > data:
            display_message("Erro", "Não é permitido editar um evento encerrado!", True)
            return
        
        view_events.destroy()
        event_window(selected_event)

    def invite_participants(selected_event):
        data_atual = str(datetime.today().date())
        data = selected_event.get_data()
             
        if data_atual > data:
            display_message("Erro", "Não é permitido convidar participantes para um evento encerrado!", True)
            return
        
        invite_participants_window(selected_event, view_events)

    def create_edit_event_function(event):
        def edit_event():
            update_event(event)
        return edit_event
    
    def create_invite_participants_function(event):
        def invite_participants_function():
            invite_participants(event)
        return invite_participants_function

    def get_registers(selected_event):  
        view_events.destroy()
        participants_window(selected_event)
   
    # preenche a tabela com os eventos do banco de dados
    global event_service
    global user_service
    events = event_service.get_all_events_by_organizer(user_service.get_logged_user().get_id())
    if len(events) == 0:
        display_message("Nenhum evento encontrado", "Você não cadastrou nenhum evento!", False)
        return
    
    view_events = tk.Toplevel(root)
    view_events.title("Visualizar Eventos")

    def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

    canvas = tk.Canvas(view_events, width=250, name="event_canvas")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(view_events, command=canvas.yview, name = "scrollbar")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    frame_container = tk.Frame(canvas)

    canvas.configure(yscrollcommand=scrollbar.set)
    frame_container.bind("<Configure>", configure_scroll_region)
    canvas.create_window((0, 0), window=frame_container)    
    
    for event in events:
        frame_event = tk.Frame(frame_container)

        event_name = event.get_titulo()
        event_data = event.get_data()

        name_event_label = tk.Label(frame_event, text=event_name)
        name_event_label.grid(row = 0, column=0, pady=3, sticky="w", padx=5)

        date_event_label = tk.Label(frame_event, text=event_data)
        date_event_label.grid(row = 1, column=0, pady=3, sticky="w", padx=5)

        edit_button = tk.Button(frame_event, text="Editar", command=create_edit_event_function(event))
        edit_button.grid(row = 0, column=1, pady=3, sticky="e", padx=5)

        checkin_button = tk.Button(frame_event, text="Check-in", command=lambda:get_registers(event)) 
        checkin_button.grid(row = 1, column=1, pady=3, sticky="e", padx=5)

        invite_button = tk.Button(frame_event, text="Convidar participantes", command=create_invite_participants_function(event))
        invite_button.grid(row = 2, column=1, pady=3, sticky="e", padx=5)

        frame_event.pack()

        separator = ttk.Separator(frame_container, orient='horizontal')
        separator.pack(fill='x')

def invite_participants_window(event, list_events_window):
    def generate_email_fields(invite_window):
        for children in invite_window.winfo_children():
            if children.winfo_name() == "show_more_button" or children.winfo_name() == "invite_button":
                children.forget()

        count_fields = 0
        while count_fields < 5:
            entry_email = tk.Entry(invite_window, name="mail" + str(random.randint(0, 1000)))
            entry_email.pack(pady=10)

            count_fields += 1
        
        show_more_button = tk.Button(invite_window, text="Inserir mais e-mails", command=lambda:generate_email_fields(invite_window), name="show_more_button") 
        show_more_button.pack(pady=10)

        invite_button = tk.Button(invite_window, text="Enviar convites", command=lambda:send_invites(invite_window, event), name="invite_button")
        invite_button.pack(pady=10)

    invite_window = tk.Toplevel(list_events_window)
    invite_window.title("Convite de participantes")
    title = tk.Label(invite_window, text="Digite os e-mails dos participantes que serão convidados:")
    title.pack()
    generate_email_fields(invite_window)

def send_invites(invite_window, event):
    global user_service
    emails = []

    for children in invite_window.winfo_children():
        if children.winfo_name().__contains__("mail") and children.get() != '':
            if children.get() == user_service.get_logged_user().get_email():
                display_message("Erro", "Remova seu próprio e-mail da lista de convidados", True)
                return
            emails.append(children.get())

    if len(emails) == 0:
        display_message("Erro", "Nenhum e-mail informado", True)
        invite_window.destroy()
        return

    users_ids = user_service.get_users_by_mail_list(emails)

    if len(users_ids[0]) > 2 and users_ids[0].find(Messages.USER_NOT_FOUND.value) != -1:
        display_message("Erro", users_ids[0], True)
        return
    
    message = invite_service.send_invites(event.get_id(), users_ids, str(datetime.now()))
    if message.find(Messages.INVITE_DUPLICATED.value) != -1:
        display_message("Convites duplicados", message, True)
        return
    display_message("Convites enviados", message, False)
    invite_window.destroy()
    
        
def delete_event(event, event_window):
    delete_event = messagebox.askokcancel(title="Remover evento", message = "Tem certeza que deseja remover o evento?")
    
    if delete_event:  
        global event_service  
        message = event_service.delete_event(event.get_id())
        
        if message == Messages.EVENT_DELETE_OK.value:
            display_message("Sucesso", message, False)
        else:
            display_message("Error", message, True)
            
        event_window.destroy()    

def update_user(user_id, is_organizer):
    global user_service
    user_service.update_user(user_id, is_organizer)
    display_message("Sucesso", "Usuário agora é organizador!", False)
    
def select_action():
    def reset():
        view_action.destroy()
        create_main_window()

    view_action = tk.Frame(root)
    view_action.pack(side="left", padx=20, pady=20)

    button_register_event = tk.Button(view_action, text="Cadastrar Evento", command=lambda:event_window(None))
    button_register_event.pack(padx=10, pady=10)

    button_view_events = tk.Button(view_action, text="Meus Eventos", command=show_user_events)
    button_view_events.pack(padx=10, pady=10)

    button_search_events = tk.Button(view_action, text="Buscar Eventos", command=filter_events_window)
    button_search_events.pack(padx=10, pady=10)

    button_close = tk.Button(view_action, text="Sair", command=reset)
    button_close.pack(pady=10)

def filter_events_window(): 
    def filter_events():
        for children in filter_events_window.winfo_children():
            if children.winfo_name() == "event_canvas" or children.winfo_name() == "separator" or children.winfo_name() == "scrollbar":
                children.destroy()
        local = entry_local.get()
        if entry_date.get() != '':
            date = entry_date.get_date().strftime("%Y-%m-%d")
        else:
            date = ''

        global event_service
        global user_service
        user_id = user_service.get_logged_user().get_id()
        events = event_service.filter_events(local, date, user_id)
        display_events_by_filter(events, filter_events_window, user_id)

    filter_events_window = tk.Toplevel(root)
    filter_events_window.title("Filtrar eventos")

    label_local = tk.Label(filter_events_window, text="Localização: ")
    label_local.pack()

    entry_local = tk.Entry(filter_events_window)
    entry_local.pack()

    label_date = tk.Label(filter_events_window, text="Data:")
    label_date.pack()

    entry_date = DateEntry(filter_events_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    entry_date.pack(padx=10, pady=10)

    button_register = tk.Button(filter_events_window, text="Buscar", command=filter_events)
    button_register.pack(pady=10)

def display_events_by_filter(events, view_events, user_id):
    if len(events) == 0:
        display_message("Nenhum evento encontrado", "Não foram encontrados eventos para o filtro informado", False)
        return

    def register_on_event(user_id, event_id):
        register_service.create_register(user_id, event_id)
        view_events.destroy()

    def remove_on_event(user_id, event_id):
        register_service.delete_register(user_id, event_id)
        view_events.destroy()

    def check_on_event(user_id, event_id):
        return register_service.check_register(user_id, event_id)
    
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas = tk.Canvas(view_events, width=170, name="event_canvas")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(view_events, command=canvas.yview, name = "scrollbar")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    frame_container = tk.Frame(canvas)

    canvas.configure(yscrollcommand=scrollbar.set)
    frame_container.bind("<Configure>", configure_scroll_region)
    canvas.create_window((0, 0), window=frame_container)

    for event in events:
        frame_event = tk.Frame(frame_container)

        event_id = event.get_id()
        event_name = event.get_titulo()
        event_data = event.get_data()
        event_description = event.get_descricao()
        event_location = event.get_local()
        event_time = event.get_horario()

        name_event_label = tk.Label(frame_event, text=event_name)
        name_event_label.pack(pady=3)

        date_event_label = tk.Label(frame_event, text=event_data)
        date_event_label.pack(pady=3)

        time_event_label = tk.Label(frame_event, text=event_time)
        time_event_label.pack(pady=3)

        description_event_label = tk.Label(frame_event, text=event_description)
        description_event_label.pack(pady=3)

        location_event_label = tk.Label(frame_event, text=event_location)
        location_event_label.pack(pady=3)

        if(check_on_event(user_id, event_id)) :
            register_button = tk.Button(frame_event, text="Cadastrar-se no evento",
                                        command=lambda: register_on_event(user_id, event_id))
        else:
            register_button = tk.Button(frame_event, text="Descadastrar do evento",
                                        command=lambda: remove_on_event(user_id, event_id))


        register_button.pack(pady=3)

        separator = ttk.Separator(frame_event, orient='horizontal', name='separator')
        separator.pack(fill='x')

        frame_event.pack()

def display_message(title, message, error):
    if error:
        messagebox.showerror(title, message)
    else:
        messagebox.showinfo(title, message)

init()
create_main_window()
root.mainloop()

# fecha a conexão com o banco de dados
#conn.close()
