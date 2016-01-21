 // definindo o  tour!
 var tour = {
     id: "splarch-welcome",
     selectors: {
         init: '#architecture',
     },
     showCloseButton: true,
     i18n: {
        nextBtn: 'Proximo',
        prevBtn: 'Anterior',
        doneBtn: "Ok",
        skipBtn: "Sair",
        closeTooltip: "Fechar",
     },
     showCloseButton: true,
     showPrevButton: true,
     steps: [
         {
             title: "Architecture",
             content: "Texto para decisões",
             target: "architecture",
             placement: "right",
             yOffset: 100,
             xOffset: -500,
             delay: 1,
             zindex: 0,
         },
         {
             title: "Auth",
             content: "Texto para arquitetura",
             target: "auth",
             placement: "right",
             yOffset: 40,
             xOffset: -500,
             delay: 1,
             zindex: 0
         },
         {
             title: "FAQ",
             content: "Realize pesquisas pelo sistema",
             target: "faq",
             placement: "right",
             xOffset: -500,
             yOffset: 30,
             zindex: 0
         },
         {
             title: "Requirement",
             content: "Texto para empresas",
             target: 'requirement',
             placement: "right",
             xOffset: -500,
             yOffset: 30,
             zindex: 0
         },
         {
             title: "Scoping",
             content: "Adicione ou modifique conteudo",
             target: 'scoping',
             placement: "right",
             xOffset: -500,
             yOffset: 40,
             zindex: 0
         },

         
     ]
 };

 // inicializa o tour
 hopscotch.startTour(tour);
 hopscotch.endTour();