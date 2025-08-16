# Encurtador de URL

## Objetivo do projeto
Simular o desenvolvimento de um sistema de uncurtador de URL como se estivesse em uma empresa de desenvolvimento de software.

## O que é um encurtador de URL
Um serviço de encurtamento de URLs é uma feramenta para transformar links longos e difícies de memorizar em versões curtas, simples e comparilhaveis.
São muito utilizados em diversos tipos de comunicação, como por exemplo campanha de marketing, onde através de um SMS, que possuem quantidade limitada de caracteres nas mensagens e com isso é necessário reduzir o tamanho do link para enviar via SMS. 
Outra possibilidade de uso são de facilitar o compartilhamento em redes sociais onde você pode direcionar um seguidor para um site ou tema específico onde você não disponha de uma forma simples para passar o link ao seguidor. 
O encurtador gera então a URL curta (link curto) e uma vez que clicado ou requisitado a URL encurtada o encurtador redireciona a requisição para a URL original.

Um exemplo muito utilizado de encurtador é o bitly. É interessante que crie uma conta grátis no bitly e conhecer o funcionamento do bitly.
Para esse documento criei o link no bit.ly `https://bit.ly/4l1jYXQ`. Esse link leva para a página de pesquisa do google sobre links encurtados.
O link encurtado tem 22 caracteres, sendo, 8 do protocolo `https://`, 7 do host e seperador da url `bit.ly/` e 6 do identificador do link no bitly. Já URl original tem por volta de 240 caracteres.
Veja abaixo a comparação entre a url original e a encurtada.

- URL original
https://www.google.com/search?q=link+encurtado&oq=link+encurtado&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORiABDIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIGCAUQRRg8MgYIBhBFGD0yBggHEEUYPdIBCDQzMTFqMGo3qAIIsAIB8QWffADq1gqNbQ&sourceid=chrome&ie=UTF-8

- Url Encurtada
https://bit.ly/4l1jYXQ

## O desafio / produto
Criar um serviço de encurtamento de URL que possa reduzir a URL original longa em uma URL curta, a finalizade é criar e utilizar  um identificador único para a URL orginal e chamar o serviço de encurtador passando o identificador único gerado, redirecionar para a URL original.
Nesse sentido, o encurtador deve atender usuários comuns que necessitem gerar e utilizar poucas URLs encurtadas, talvez apenas uma, ou ainda usuários profissionais que necessitem gerar e utilizar muitas URLs encurtadas.

### Primeiros passos
Antes de iniciar a implmentação do código pense como será a aplicação, tais como:
- Como gerar um identificador único para a URL original? Isso pode ser um pouco complexo a princípio e por isso já vou deixar algumas possíveis soluções você pode escolher para onde ir.
    - Existe a possibilidade de criar um algoritmo próprio, porém, quanto menor for a quantidade de caracteres do identificador único, mais complexo pode ser o algoritmo para gerar esse identificador único. Uma implementação simples seria criar um identificador incremental (exemplo: 1,2,3...n) e e aplique um conversor utilizando uma base alfanumérica curta a exemplo do base62 (09-,A-Z,a-z)
    - Já existem algumas bibliotecas prontras para esse tipo de identificador único e curto exemplo sqids.org
- Quais os dados serão solicitados ao usuário para gerar uma URL encurtada?
- Como o encurtador fará para ao receber uma requisição a partir de uma URL encurtada, redirecionar a requisição para a URL original?
- Qual arquitetura e quais tecnologias linguagens de programação, frameworks e outras ferramentas que serão utilizadas para concepção do serviço?
    -OBS: Aqui é importante estudar quais as arquiteturas e tecnologias podem ser empregadas num encurtador de URL mesmo que não conheça as tecnologias
- Quais os requisitos não funcionais que aplicação precisará ter?
- Como será o acompanhamento do projeto e suas tarefas e será feito em etapas? Por onde começar, o que foi concluído, o que falta fazer, qual a previsão de conclusão das tarefas e projeto?
- Onde será disponibilizado o serviço e quais seriam os custos estimados mediante as tecnologias que serão empregadas?

### Etapas
1. Criar uma proposta de implementação para o projeto, mediante o que foi exposto na seção `Primeiros passos`;
    - Essa primeira etapa é necessária para discutir soluções com alguém com mais experiência com desenvolvimento de software com a finalidade de produzir uma solução robusta e dentro das possibilidades de um serviço minimamente viável (MVP - Minimum Viable Product)
    - OBS: Essa seção de `Primeiros passos` é só uma sugestão, pode-se sugerir outras funcionalidades ou abordagens que pretende seguir para o projeto de encurtador
2. Escolher uma ferramenta livre para acompanhamento do projeto;
3. Desenvolver e melhorar a ferramenta para realizar encurtamento de URLs;
4. Disponibilizar a aplicação online
    