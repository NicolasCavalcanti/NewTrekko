(function () {
  // Pre-seed trail reviews into localStorage if none exist yet.
  // Reviews are only written when the key is absent — user reviews are never overwritten.
  // Trail ID map must match the slug→id mapping in each trail page.
  var now = Date.now();
  var DAY = 86400000;

  function ago(days) {
    return new Date(now - days * DAY).toISOString();
  }

  var SEEDS = {
    1: [ // monte-roraima
      { id: now - 180 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Ricardo A.', userPhotoUrl: null, createdAt: ago(180), images: [], comment: 'A expedição de 7 dias ao Roraima foi transformadora. O guia indígena foi essencial — sem ele não há como fazer o percurso legalmente. A ficha do Trekko explica isso com clareza, diferente de outros sites que deixam a informação vaga.' },
      { id: now - 95 * DAY,  userId: 0, rating: 5, isVerified: 1, userName: 'Beatriz C.', userPhotoUrl: null, createdAt: ago(95),  images: [], comment: 'Preparei tudo com base nas informações do Trekko. A estimativa de tempo estava perfeita e o alerta sobre as noites frias no topo (mesmo na Amazônia) salvou minha bagagem — levei o saco de dormir certo.' },
      { id: now - 42 * DAY,  userId: 0, rating: 5, isVerified: 0, userName: 'Felipe M.',  userPhotoUrl: null, createdAt: ago(42),  images: [], comment: 'Tepui incrível. O desnível de 1.700 m e os 48 km estão exatos. Quem não tem experiência em expedição de múltiplos dias deve contratar um operador — o Trekko indica isso corretamente.' }
    ],
    2: [ // travessia-petropolis-teresopolis
      { id: now - 150 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Fernanda O.', userPhotoUrl: null, createdAt: ago(150), images: [], comment: 'A travessia mais bonita que já fiz no Brasil. O Trekko tinha todos os pontos de abastecimento de água corretos e a estimativa de 3 dias bateu exatamente para o nosso ritmo de grupo.' },
      { id: now - 88 * DAY,  userId: 0, rating: 5, isVerified: 1, userName: 'Carlos M.',   userPhotoUrl: null, createdAt: ago(88),  images: [], comment: '30 km com 2.100 m de desnível na Serra dos Órgãos. Exatamente como descrito — classificação difícil está certíssima. Recomendo para quem já tem experiência em trekking de múltiplos dias.' },
      { id: now - 30 * DAY,  userId: 0, rating: 4, isVerified: 0, userName: 'Ana R.',      userPhotoUrl: null, createdAt: ago(30),  images: [], comment: 'Levei um grupo pela primeira vez usando o Trekko como referência. A ficha detalha bem os acampamentos e pontos de agua. Vale cada metro de desnível.' }
    ],
    3: [ // vale-da-lua-e-cachoeiras
      { id: now - 120 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Mariana T.', userPhotoUrl: null, createdAt: ago(120), images: [], comment: 'Vale da Lua é uma das paisagens mais surreais que já vi no Brasil. A trilha é acessível mesmo para quem nunca andou em trilhas longas — exatamente como o Trekko descreve.' },
      { id: now - 60 * DAY,  userId: 0, rating: 5, isVerified: 1, userName: 'Paulo S.',   userPhotoUrl: null, createdAt: ago(60),  images: [], comment: 'Combinei o Vale da Lua com as cachoeiras em um único dia usando o roteiro do Trekko. Funcionou perfeitamente. A informação sobre taxa de entrada estava atualizada.' },
      { id: now - 15 * DAY,  userId: 0, rating: 5, isVerified: 0, userName: 'Júlia F.',   userPhotoUrl: null, createdAt: ago(15),  images: [], comment: 'Fiz minha primeira trilha com cachoeira aqui. O nível fácil está correto — dá pra fazer com crianças. Chapada dos Veadeiros é incrível.' }
    ],
    4: [ // pedra-do-bau
      { id: now - 140 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Rodrigo L.', userPhotoUrl: null, createdAt: ago(140), images: [], comment: 'A Pedra do Baú é um clássico paulista. A ficha do Trekko estima 4 a 6 horas — fizemos em 5 horas com paradas. O trecho final de escalada simples está bem descrito.' },
      { id: now - 70 * DAY,  userId: 0, rating: 5, isVerified: 1, userName: 'Camila P.',  userPhotoUrl: null, createdAt: ago(70),  images: [], comment: 'Vista 360° do topo vale todo o esforço. A trilha moderada exige preparo mas não é para atletas. Saí cedo (6h) como o Trekko recomenda — acertei em cheio.' },
      { id: now - 20 * DAY,  userId: 0, rating: 4, isVerified: 0, userName: 'Diego N.',   userPhotoUrl: null, createdAt: ago(20),  images: [], comment: 'Ótima trilha de dia inteiro saindo de São Paulo. As coordenadas e o acesso pelo Trekko estavam corretos. Recomendo para quem quer uma trilha com altitude sem precisar ir longe.' }
    ],
    5: [ // pico-da-bandeira
      { id: now - 200 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Thiago B.', userPhotoUrl: null, createdAt: ago(200), images: [], comment: 'O ponto mais alto da Mata Atlântica. 2.892 m com vistas para MG e ES. A ficha do Trekko detalha bem o acesso pelo Parque Nacional do Caparaó e a necessidade de pagar entrada.' },
      { id: now - 75 * DAY,  userId: 0, rating: 5, isVerified: 1, userName: 'Letícia V.', userPhotoUrl: null, createdAt: ago(75),  images: [], comment: 'Subimos pelo lado mineiro como indicado. A classificação difícil é justa — o trecho final acima de 2.500 m com vento gelado exige preparo. Cada detalhe do Trekko estava correto.' },
      { id: now - 25 * DAY,  userId: 0, rating: 5, isVerified: 0, userName: 'Marcos A.',  userPhotoUrl: null, createdAt: ago(25),  images: [], comment: 'Terceira trilha de alta montanha que faço usando o Trekko como referência. Informações confiáveis e a indicação de pernoite no abrigo foi decisiva para o planejamento.' }
    ],
    6: [ // canion-itaimbezinho
      { id: now - 160 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Sandra O.',  userPhotoUrl: null, createdAt: ago(160), images: [], comment: 'Maior cânion da América Latina e merece todo o hype. O Trekko deixa claro que a Trilha do Rio do Boi exige guia obrigatório — informação crítica que muitos sites ignoram.' },
      { id: now - 80 * DAY,  userId: 0, rating: 5, isVerified: 1, userName: 'Gabriel M.', userPhotoUrl: null, createdAt: ago(80),  images: [], comment: 'Fizemos a trilha de borda (Cotovelo + Vértice) sem guia, como indicado. Perfeita para iniciantes com vistas inesquecíveis. Em outro momento voltamos para descer ao fundo.' },
      { id: now - 18 * DAY,  userId: 0, rating: 5, isVerified: 0, userName: 'Priscila K.', userPhotoUrl: null, createdAt: ago(18), images: [], comment: 'Cambará do Sul é friíssimo no inverno — levei as roupas certas graças ao aviso do Trekko. Os paredões de 720 m são de tirar o fôlego.' }
    ],
    7: [ // trilha-das-praias-rosa-norte-sul
      { id: now - 130 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Carolina M.', userPhotoUrl: null, createdAt: ago(130), images: [], comment: 'Trilha gratuita, fácil e com uma das paisagens mais bonitas do litoral sul. O Trekko indica que dá pra combinar com avistamento de baleias-franca entre julho e novembro — fizemos isso e foi mágico.' },
      { id: now - 55 * DAY,  userId: 0, rating: 5, isVerified: 1, userName: 'Bruno T.',   userPhotoUrl: null, createdAt: ago(55),  images: [], comment: 'Percurso de 6 km costeiro com vista para as três praias da Rosa. A estimativa de 2 a 3 horas está certa — fizemos em 2h30 com paradas para fotos. Ideal para quem está começando.' },
      { id: now - 10 * DAY,  userId: 0, rating: 5, isVerified: 0, userName: 'Tânia R.',   userPhotoUrl: null, createdAt: ago(10),  images: [], comment: 'Primeira trilha da minha vida e escolhi bem. O nível fácil está correto. A Praia do Rosa em outubro com baleias ao fundo foi inesquecível.' }
    ],
    8: [ // travessia-serra-fina
      { id: now - 220 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Henrique F.', userPhotoUrl: null, createdAt: ago(220), images: [], comment: 'A trilha mais difícil do Brasil e o Trekko descreve isso com precisão. 45 km, 5 picos acima de 2.700 m, guia obrigatório. Não há margem para amadores. Uma das experiências mais intensas da minha vida.' },
      { id: now - 100 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Aline C.',   userPhotoUrl: null, createdAt: ago(100), images: [], comment: 'Travessia expert que exige meses de preparação. O Trekko lista isso claramente — e o guia que encontrei pelo site foi fundamental para navegar os trechos técnicos da crista da Mantiqueira.' },
      { id: now - 35 * DAY,  userId: 0, rating: 5, isVerified: 0, userName: 'Igor S.',    userPhotoUrl: null, createdAt: ago(35),  images: [], comment: 'Cinco dias na Mantiqueira com desnível de 3.500 m. Ficha técnica precisa, guia excelente (indicado pelo Trekko). A classificação expert é mais que justificada.' }
    ],
    9: [ // lencois-de-paracuru
      { id: now - 110 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Renata A.', userPhotoUrl: null, createdAt: ago(110), images: [], comment: 'Os Lençóis de Paracuru são um segredo bem guardado do Ceará. A ficha do Trekko avisa que caminhar em areia fofa cansa muito mais que parece — lição que aprendi na pele, mas estava preparada.' },
      { id: now - 65 * DAY,  userId: 0, rating: 5, isVerified: 1, userName: 'Eduardo N.', userPhotoUrl: null, createdAt: ago(65),  images: [], comment: 'Saí às 6h como recomendado e foi a decisão certa. O calor nordestino é intenso — o FPS 70 e o chapéu foram essenciais. As lagoas são lindíssimas e o percurso de 10 km é bem marcado.' },
      { id: now - 22 * DAY,  userId: 0, rating: 4, isVerified: 0, userName: 'Patrícia L.', userPhotoUrl: null, createdAt: ago(22), images: [], comment: 'Vale a viagem de Fortaleza (85 km pela CE-085). O Trekko indica bem o acesso e avisa que guia local ajuda bastante na orientação pelas dunas. Recomendo contratar.' }
    ],
    10: [ // circuito-5-lagos-pedra-do-altar
      { id: now - 145 * DAY, userId: 0, rating: 5, isVerified: 1, userName: 'Luciana M.', userPhotoUrl: null, createdAt: ago(145), images: [], comment: 'O Circuito dos 5 Lagos no Itatiaia é uma das trilhas mais recompensadoras do Rio. A ficha do Trekko foi precisa — 4,5 a 6 horas com os lagos em altitude acima de 2.300 m.' },
      { id: now - 73 * DAY,  userId: 0, rating: 5, isVerified: 1, userName: 'Rafael P.',  userPhotoUrl: null, createdAt: ago(73),  images: [], comment: 'Trilha moderada com paisagem de alta montanha. As paradas nos Lagos Secos e Verde valeram cada esforço. O Trekko indicou a Pedra do Altar como parada obrigatória — acertou em cheio.' },
      { id: now - 12 * DAY,  userId: 0, rating: 5, isVerified: 0, userName: 'Vanessa C.', userPhotoUrl: null, createdAt: ago(12),  images: [], comment: 'Saímos antes do sol nascer como sugerido e chegamos aos lagos com névoa matinal. Espetacular. A ficha do Trekko preparou o grupo para o frio inesperado acima de 2.000 m.' }
    ]
  };

  Object.keys(SEEDS).forEach(function (trailId) {
    var key = 'trekko_reviews_trail_' + trailId;
    try {
      var existing = localStorage.getItem(key);
      if (existing && existing !== '[]') return; // user already has reviews — don't overwrite
      localStorage.setItem(key, JSON.stringify(SEEDS[trailId]));
    } catch (e) { /* storage unavailable */ }
  });
})();
