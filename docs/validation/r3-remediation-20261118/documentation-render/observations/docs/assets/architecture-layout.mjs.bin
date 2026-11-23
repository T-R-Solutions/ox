/** Designed composition of architecture.mmd; Lucide geometry stays unchanged. */
export function architectureSvg(pack) {
 const esc = text => text.replaceAll('&','&amp;').replaceAll('<','&lt;');
 const icon = (name,x,y) => `<g transform="translate(${x} ${y}) scale(1.4)" color="#4338ca">${pack.icons[name].body}</g>`;
 const text = (x,y,label,size=18,weight=400) => `<text x="${x}" y="${y}" font-size="${size}" font-weight="${weight}" fill="#172554">${esc(label)}</text>`;
 const box = (x,y,w,h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="#ffffff" stroke="#6366f1" stroke-width="1.5"/>`;
 const card = (x,y,w,h,name,label,sub) => box(x,y,w,h)+icon(name,x+16,y+18)+text(x+60,y+40,label,18,700)+text(x+18,y+h-20,sub,15);
 let svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 744" role="img" aria-labelledby="title desc"><title id="title">Arquitetura executável da fundação local</title><desc id="desc">Desktop Iced chama Controller. O Controller coordena Agent Runtime e Verification Engine no processo Ox. Runtime supervisiona o produtor local-task. Engine executa o oráculo task-oracle. O produtor escreve os arquivos da tentativa, lidos pelo oráculo. Plugin Host permanece uma API independente da UI.</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#475569"/></marker></defs><rect width="960" height="744" fill="#fff"/><g font-family="Arial,sans-serif">';
 svg+='<rect x="24" y="24" width="912" height="376" rx="16" fill="#f8fafc" stroke="#64748b"/>'+text(48,60,'PROCESSO OX · coordenação e estado em memória',20,700);
 svg+='<rect x="24" y="432" width="912" height="164" rx="16" fill="#f8fafc" stroke="#64748b" stroke-dasharray="6 4"/>'+text(350,454,'PROCESSOS FILHOS',18,700);
 svg+=card(80,96,220,104,'monitor','Desktop Iced','Ações e estados da UI');
 svg+=card(360,96,240,104,'workflow','Controller','Uma tentativa por vez');
 svg+=card(80,264,236,112,'cpu','Agent Runtime','Supervisão do filho direto');
 svg+=card(660,264,236,112,'clipboard-check','Verification Engine','Snapshots e observações');
 svg+=card(80,480,236,100,'terminal','local-task','Produtor controlado');
 svg+=card(660,480,236,100,'scan-search','task-oracle','Verificador independente');
 svg+=box(330,620,300,100)+icon('folder-open',350,640)+text(394,662,'Arquivos da tentativa',18,700)+text(350,696,'request.txt · result.txt',16);
 const edge=d=>`<path d="${d}" fill="none" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>`;
 svg+=edge('M300 148H360')+text(309,132,'ações',16);
 svg+=edge('M480 200V228H198V264')+text(245,248,'executar / cancelar',15);
 svg+=edge('M480 228H778V264')+text(500,248,'verificar / atualizar',15);
 svg+=edge('M198 376V480')+text(214,418,'supervisiona',15);
 svg+=edge('M778 376V480')+text(616,418,'executa e observa',15);
 svg+=edge('M198 580V670H330')+text(76,646,'produz resultado',15);
 svg+=edge('M630 670H778V580')+text(790,630,'lê inputs',15);
 svg+='</g></svg>';
 return svg+'\n';
}
