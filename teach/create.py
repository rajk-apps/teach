from . import models
from django.shortcuts import redirect
from django.urls import reverse

def logiccourse(request):
    try:
        past = models.Course.objects.get(pk='prelog')
        lecs = past.lectures.all()
        slides = [lec.slides.all() for lec in lecs]
        conts = [slide.contents.all() for slideset in slides for slide in slideset]
        past.delete()
        lecs.delete()
        [slide.delete() for slide in slides]
        [cont.delete() for cont in conts]
    except:
        print("NOPAST")
    
    logic_course = models.Course('Pre-Logika kurzus',
                          'Formális logika alapozó',
                          'prelog')
    
    logic_course.save()
    
    prelog_lecture = models.Lecture('Pre-logika kurzusalkalom',
                                    'Logika alapozó előadás',
                                    'prelog1')
    
    prelog_lecture.save()
    
    models.CourseStructure(ordernum=1,course=logic_course,lecture=prelog_lecture).save()
    
    
    CONT1 = """[{'t':'r','ch':[
        {'t':'c','w':12,'ch':[
                {'t':'n','s':'','m':s[0]}
                ]}
            ]}
        ]"""
    
    R2 = """[{'t':'r','ch':[
        {'t':'c','w':12,'ch':[
                {'t':'n','s':'%s','m':s[0]}
                ]}
            ]},
        {'t':'r','ch':[
        {'t':'c','w':12,'ch':[
                {'t':'n','s':'%s','m':s[1]}
                ]}
            ]}
        ]"""
    
    slide0 = models.Slide('Miről beszélünk?','prelog:q',CONT1,hastitle=False)
    
    slide1 = models.Slide('Ítéletlogika','prelog:nullog',R2 % ("font-size:1.7vw;","font-size:1.4vw;"))
    
    slide2 = models.Slide('Műveletek','prelog:muvs',CONT1)
    
    slide3 = models.Slide('Példák','prelog:muvs-exs',R2 % ("font-size:1.7vw;","font-size:1.4vw;"))
    
    slide4 = models.Slide('Igazságtáblázat','prelog:truthtab',CONT1)
    
    slide5 = models.Slide('Tételek','prelog:tauts',R2)
    
    slide6 = models.Slide('Tétel-e?','prelog:tautq',CONT1)
    
    slide7 = models.Slide('Elsőrendű logika','prelog:firstord',CONT1)
    
    slide8 = models.Slide('Predikátumok','prelog:predics',CONT1)
    
    slide9 = models.Slide('Kvantorok','prelog:quantis',CONT1)
    
    slide10 = models.Slide('Nyitott és zárt formulák','prelog:formulas',R2)
    
    slide11 = models.Slide('Példák','prelog:formulas-ex',R2)
    
    i = 1
    
    for slide in [slide0,slide1,slide2,slide3,slide4,slide5,slide6,slide7,
                  slide8,slide9,slide10,slide11]:
        slide.save()
        models.LectureStructure(ordernum=i,slide=slide,lecture=prelog_lecture).save()
        i += 1
    
    content_log_q = models.Content('Mi a formális logika?','logic:whatis','''
## Mi a formális logika?

Matematikához hasonló szabályrendszer, nyelv aminek fókuszában állítások vannak <!-- .element: class="fragment" -->
''')
    
    content_nullog = models.Content('Ítéletlogika','logic:nullog','''
- Logikai változók, kifejezések igazságértékével foglalkozik
- Csak IGAZ vagy HAMIS állítás létezik
- Változók között létezhetnek logikai műveletek
''')
    
    content_logvar_def = models.Content('Logikai változó','prelog:def','''
#### Logikai változó
Olyan változó mely egyedül az IGAZ és a HAMIS értékeket veheti fel.
pl. kijelentő mondat, matematikai kifejezés, utasításhoz kötött feltétel
''')
    
    content_oper_list = models.Content('Műveletek','logic:operations','''
- $\\neg$: tagadás
- $\land$: és (konjukció)
- $\lor$: vagy (diszjunkció)
- $\Rightarrow$: implikáció
- $\Leftrightarrow$: ekvivalencia
''')
    
    content_algebra_q = models.Content('Mire hasonlít mindez?','logic:algebraq','''
- változók
- meghatározott lehetséges értékek amiket változó felvehet
- változók közötti műveletek
- algebra!
''')
    
    content_var_example = models.Content('Kijelentések:','prelog:varex','''
A: Dávid okos, B: Dávid tudja ki 2008 aranylabdása, C: Dávid szereti a fagyit, D: kevesen tudják ki 2008 aranylabdása
''')
    
    content_ex_formula_list = models.Content('Formulává alakítható','logic:exformulas','''
1. Dávid okos és tudja ki 2008 aranylabdása
  - A $\land$ B <!-- .element: class="fragment" -->
1.  Dávid nem szereti a fagyit de okos
  - $\\neg$ C $\land$ A <!-- .element: class="fragment" -->
1.  Akkor tudják kevesen ki 2008 aranylabdása, ha Dávid tudja és okos
  - D $\Leftarrow$ (B $\land$ A) <!-- .element: class="fragment" -->
1.  Dávid akkor és csakis akkor okos, ha tudja ki 2008 aranylabdása és ezt kevesen tudják
  - A $\Leftrightarrow$ (B $\land$ D) <!-- .element: class="fragment" -->
1.  Ha kevesen tudják ki 2008 aranylabdása, Dávid nem tudja
  - D $\Rightarrow$ $\\neg$ B <!-- .element: class="fragment" -->
''')
    
    content_truthtable = models.Content('Igazságtábla','logic:truthtable','''
A | B | $\\neg$ A | A $\land$ B | A $\lor$ B | A $\Rightarrow$ B | A $\Leftrightarrow$  B
--- | --- | --- | --- | --- | --- | ---
I | I | H <!-- .element: class="fragment" data-fragment-index="1" --> | I <!-- .element: class="fragment" data-fragment-index="2" -->  | I <!-- .element: class="fragment" data-fragment-index="3" -->  | I <!-- .element: class="fragment" data-fragment-index="4" -->  | I <!-- .element: class="fragment" data-fragment-index="5" --> |
I | H | H <!-- .element: class="fragment" data-fragment-index="1" --> | H <!-- .element: class="fragment" data-fragment-index="2" -->  | I <!-- .element: class="fragment" data-fragment-index="3" -->  | H <!-- .element: class="fragment" data-fragment-index="4" -->  | H <!-- .element: class="fragment" data-fragment-index="5" --> |
H | I | I <!-- .element: class="fragment" data-fragment-index="1" --> | H <!-- .element: class="fragment" data-fragment-index="2" -->  | I <!-- .element: class="fragment" data-fragment-index="3" -->  | I <!-- .element: class="fragment" data-fragment-index="4" -->  | H <!-- .element: class="fragment" data-fragment-index="5" --> |
H | H | I <!-- .element: class="fragment" data-fragment-index="1" --> | H <!-- .element: class="fragment" data-fragment-index="2" -->  | H <!-- .element: class="fragment" data-fragment-index="3" -->  | I <!-- .element: class="fragment" data-fragment-index="4" -->  | I <!-- .element: class="fragment" data-fragment-index="5" --> |

''')
    
    content_tautology_def = models.Content('Tétel','logic:tautdef','''
olyan formulák amik a bennük szereplő kifejezések igazságértékétől függetlenül igazak
''')
    
    content_tautology_list = models.Content('Tételek','logic:tautlist','''
- asszociativitás:
  - $A \lor (B \lor C) \Leftrightarrow (A \lor B) \lor C$
- disztributivitás:
  - $A \land (B \lor C) \Leftrightarrow (A \land B) \lor (A \land C)$
- De Morgan szabály:
  - $\\neg (A \lor B) \Leftrightarrow \\neg A \land \\neg B$
- szillogizmus:
  - $(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$
''')
    
    content_tautology_q = models.Content('Tétel-e?','logic:tautq','''
1.  $A \Rightarrow B \Leftrightarrow \\neg A \lor B$
1.  $(A \Rightarrow B) \lor (B \Rightarrow A)$
''')
    
    content_firstord_atts = models.Content('Elsőrendű logika','logic:firstordatts','''
1.  Predikátumok
  - változót tartalmazó kifejezés
  - a benne szereplő változó(k)tól függ az igazságértéke
2.  Kvantorok
  - $\\forall$ "mindegyik"
  - $\exists$ "létezik"
''')
    
    content_predicate_exs = models.Content('Predikátumok','logic:predicexs1','''
1. egyváltozós
  - $P$: "páros szám"
  - $P(x)$ akkor igaz ha $x$ páros
2. többváltozós
  - $NE$: "nagyobb egyenlő"
  - $NE(x,y)$ akkor igaz ha $x \geq y$, különben hamis
3. formulában
  - $NE(x,y) \land P(y)$
  - $NE(x,y) \Rightarrow NE(y,x)$
''')
    
    content_quantifier_exs = models.Content('Kvantorok','logic:quantexs','''
1.  $\\forall$
1.  $\exists$

Formulában:
1.  $\\forall x ( P(2x) )$
1.  $\\forall x ( \exists y (NE(x,y)))$
1.  $\\nexists x (\\neg NE(x,x))$
''')
    
    content_fixvar_def = models.Content('Kötött változó','prelog:fvdef','''
Ha egy kijelentésben egy változó minden előfordulása valamilyen kvantor hatáskörében van, akkor azt mondjuk, hogy a változó **kötött**, különben **szabad**
''')
    
    content_closeform_def = models.Content('Zárt formula','prelog:cfdef','''
Az a formula, aminek nincs szabad változója. Máskülönben nyitott formula
''')
    
    content_predexs = models.Content('Predikátumok:','logic:predicexs2','''
$F(x)$: $x$ férfi, $N(x)$: $x$ nő, $V(x,y)$: $x$ vonzónak tartja $y$-t
''')
    
    content_predexs_task = models.Content('Kifejezni predikátumokkal','logic:predictsk','''
1.  $d$-nek minden nő tetszik
1.  $k$ egy biszexuális nő
1.  léteznek aszexuális emberek
1.  mindenki biszexuális
1.  csak a férfiak között vannak melegek
''')
    
    for content in [content_log_q,content_nullog,
                    content_logvar_def,content_oper_list,
                    content_algebra_q,content_var_example,
                    content_ex_formula_list,content_truthtable,
                    content_tautology_def,content_tautology_list,
                    content_tautology_q,content_firstord_atts,
                    content_predicate_exs,content_quantifier_exs,
                    content_fixvar_def,content_closeform_def,
                    content_predexs,content_predexs_task]:
        content.save()
    
    models.SlideStructure(slide=slide0,
                          content=content_log_q,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide1,
                          content=content_nullog,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide1,
                          content=content_logvar_def,
                          ordernum=2).save()
    
    models.SlideStructure(slide=slide2,
                          content=content_oper_list,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide3,
                          content=content_var_example,
                          ordernum=1).save()
                          
    models.SlideStructure(slide=slide3,
                          content=content_ex_formula_list,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide4,
                          content=content_truthtable,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide5,
                          content=content_tautology_def,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide5,
                          content=content_tautology_list,
                          ordernum=2).save()
    
    models.SlideStructure(slide=slide6,
                          content=content_tautology_q,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide7,
                          content=content_firstord_atts,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide8,
                          content=content_predicate_exs,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide9,
                          content=content_quantifier_exs,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide10,
                          content=content_fixvar_def,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide10,
                          content=content_closeform_def,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide11,
                          content=content_predexs,
                          ordernum=1).save()
    
    models.SlideStructure(slide=slide11,
                          content=content_predexs_task,
                          ordernum=1).save()
    
    return redirect(reverse('teach:home'))