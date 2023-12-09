#biblioteca para criar as interfaces gráficas
import tkinter as tk

#captura de tecla
from pynput.keyboard import Listener

#realizar operações de expressões regulares
import re

#executar o processo de captura de teclas em uma thread separada
import threading

#usada para armazenar as palavras capturadas
captured_words = []

'''esta função processa as teclas pressionadas e adiciona o resultado ao final da lista captured_words
as substituições realizadas com expressões regulares servem para formatar as teclas capturadas de maneira 
mais fácil de entender, por exemplo, substituindo Key.space por um espaço em branco e Key.enter por uma quebra de linha'''
def capturar(tecla):
    global captured_words
    tecla = str(tecla)
    tecla = re.sub(r'\'', '', tecla)
    tecla = re.sub(r'Key.space', ' ', tecla)
    tecla = re.sub(r'Key.enter', '\n', tecla)
    tecla = re.sub(r'Key.*', '', tecla)
    captured_words.append(tecla)

'''esta função inicia a captura de teclas usando a biblioteca pynput.keyboard.Listener. 
quando chamada, ela atualiza o rótulo capturar_status para informar que a captura está em
 andamento e inicia o processo de captura de teclas'''
def iniciar_captura():
    with Listener(on_press=capturar) as l:
        capturar_status.config(text="Capturando teclas...")
        l.join()

'''esta função inicia o processo de captura de teclas em uma nova thread, permitindo que a interface grafica
criada continue respondendo enquanto a captura está acontecendo'''
def iniciar_captura_automaticamente():
    thread_captura = threading.Thread(target=iniciar_captura)
    thread_captura.daemon = True
    thread_captura.start()

'''esta função é responsável por atualizar o conteúdo exibido na janela da interface grafica
 com o texto capturado. Ela remove o conteúdo anterior e insere o novo texto, a cada 100ms, 
 usando a função after do tkinter'''
def atualizar_texto():
    global captured_words
    palavras_juntas = ''.join(captured_words)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, palavras_juntas)
    # Atualizar o texto a cada 100ms
    app.after(100, atualizar_texto)

#cria uma instância da classe Tk, que representa a janela principal da interface grafica
app = tk.Tk()

#titulo da interface grafica
app.title("Captura de Teclas")

#tamanh da interface grafica
app.geometry("500x400")

'''cria um widget de texto multilinha na janela app, o argumento wrap=tk.WORD indica que as 
palavras serão quebradas para a próxima linha quando necessario, em vez de quebrar o texto no meio das palavras'''
output_text = tk.Text(app, wrap=tk.WORD)

'''empacota o widget de texto para preencher o espaço disponível na janela, tanto na direção horizontal(X) 
quanto na direção vertical(Y)'''
output_text.pack(expand=True, fill=tk.BOTH)

'''cria uma barra de rolagem vertical associada ao widget de texto output_text. Isso permite que o usuário role 
verticalmente pelo conteudo do widget de texto'''
scrollbar = tk.Scrollbar(app, command=output_text.yview)

#configura o widget de texto para usar a barra de rolagem scrollbar para controlar a rolagem vertical
output_text.config(yscrollcommand=scrollbar.set)

#empacota a barra de rolagem a direita da janela e faz com que ela preencha o espaço vertical disponível
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#essa funcao e chamada para iniciar a captura automatica das teclas digitadas pelo usuário
iniciar_captura_automaticamente()

#essa funcao e chamada para atualizar o texto
atualizar_texto()

#cria um rotulo que sera exibido na janela
capturar_status = tk.Label(app, text="Captura de teclas em andamento...")

#empacota o rotulo na janela
capturar_status.pack()

''' Inicia o loop principal da aplicao, que permite que a interface grafica responda aos eventos do usuario
 e do sistema operacional, como a captura de teclas e atualizacao do conteúdo do widget de texto'''
app.mainloop()