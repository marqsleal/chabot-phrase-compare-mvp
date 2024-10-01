from regex import normalizar_texto

def main():
    perguntas_respostas = {
        'Qual é o horário de funcionamento?': 'Estamos abertos de segunda a sexta, das 9h às 18h. Aos sábados, das 9h às 14h. Fechamos aos domingos e feriados.',
        'Onde vocês estão localizados?': 'Estamos localizados na Avenida Principal, 123, no centro da cidade.',
        'Quais formas de pagamento vocês aceitam?': 'Aceitamos cartão de crédito, débito, Pix e transferência bancária.',
        'Quais serviços vocês oferecem?': 'Oferecemos uma variedade de serviços, incluindo consultoria, desenvolvimento de software e suporte técnico. Posso ajudar com mais informações sobre algum desses?',
        'Como funciona a política de devoluções?': 'Você pode devolver qualquer produto em até 30 dias após a compra, desde que esteja nas mesmas condições em que foi entregue. Para iniciar uma devolução, entre em contato com nosso suporte.',
        'Estou com problemas no meu pedido. O que devo fazer?': 'Peço desculpas pelo inconveniente! Por favor, envie o número do pedido e uma breve descrição do problema. Nossa equipe de suporte entrará em contato em breve.',
        'Quanto tempo demora a entrega?': 'O prazo de entrega varia de acordo com sua localização. Em média, leva de 3 a 7 dias úteis para entregas dentro do Brasil.',
        'Como faço para me cadastrar?': 'Você pode se cadastrar diretamente no nosso site, clicando no botão "Registrar-se." Basta preencher o formulário com seus dados e criar uma senha segura.',
        'Vocês têm alguma promoção no momento?': 'Sim! Estamos com descontos especiais em nossos principais serviços. Confira nossa página de promoções para mais detalhes.',
        'Como posso deixar um feedback?': 'Agradecemos por querer nos dar um feedback! Você pode preencher nosso formulário de satisfação no site ou enviar um e-mail diretamente para feedback@empresa.com.'
    }
    for pergunta, resposta in perguntas_respostas.items():
        print(f'{normalizar_texto(pergunta)}\n{normalizar_texto(resposta)}\n\n')

if __name__ == '__main__':
    main()
