"""
Salva as variáveis tk.BooleanVar.
Ela é uma variável boolean normal, mas é ligada a um master. Dependendo de como o usuário interage com o CheckButton, o valor dela é alterado.
cbValues existe para centralizar todas essas variáveis em um só ponto. Ao iniciar a variável, eu coloco ela no dicionário e depois atribuo a ela um master. A partir disso, o usuário pode alterar a variável dentro do vetor, já que ela está ligada ao CheckButton.
"""
cbValues = {}

"""
Salva os ids que foram selecionados.
Depois disso, eu posso iterar a lista para qualquer necessidade.
"""
cbIds = []