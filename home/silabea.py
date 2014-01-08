# -*- coding: utf-8 -*- 
#! /usr/bin/python

"""
	http://www.fismat.umich.mx/~karina/tesisLicenciatura/capitulo2.html
	http://es.wikipedia.org/wiki/S%C3%ADlaba
	http://liceu.uab.es/~joaquim/phonetics/fon_esp/silaba_espanol.html
	http://es.wikipedia.org/wiki/Hiato_(fonolog%C3%ADa)
	http://www.galeon.com/la-poesia/ortograf.pdf
	http://es.wikipedia.org/wiki/Di%C3%A9resis
	http://es.wikipedia.org/wiki/Diptongo
	http://es.wikipedia.org/wiki/Triptongo
	http://www.rae.es/consultas/palabras-como-guion-truhan-fie-liais-etc-se-escriben-sin-tilde
	
"""


def silabas(palabra):
	silabas = []
	letra = 0
	salto = 0
	
	palabra = minusculas(palabra)

	while True:
		try:
			if letra >= len(palabra): break
			silaba = ""
			salto = 0
			
			if consonante(palabra[letra]):
				if guegui(palabra[letra+salto:]): # esto es una chapu, pero no tengo otra forma por ahora :(
					salto += 2
				elif ataque_complejo(palabra[letra:letra+2]):
					salto += 2
				else:
					salto += 1
			else:
				salto += 0 # vocal
			
			if triptongo(palabra[letra+salto:]):
				salto += 3
			elif diptongo_con_h(palabra[letra+salto:]):
				salto += 3
			elif diptongo(palabra[letra+salto:]):
				salto += 2
			elif dieresis(palabra[letra+salto:]):
				salto += 2
			else:
				salto += 1

			#if coda_compleja(palabra[letra+salto:]):
			#	salto += 2
			#elif coda_simple(palabra[letra+salto:]):
			#	salto += 1
			salto += coda(palabra[letra+salto:])

			
			silaba = palabra[letra:letra+salto]
			letra += salto

			silabas.append(silaba)
			#print silabas, silaba, letra, salto, "--"
			#time.sleep(2)
		except IndexError:
			break

	return silabas


def vocal(letra):
	return True if letra in [u'a', u'e', u'i', u'o', u'u', u'á', u'é', u'í', u'ó', u'ú', u'ü'] else False

def consonante(letra):
	return not vocal(letra)


def ataque_complejo(c):
	if len(c) < 2: return False
	return True if (c[0] in [u'b', u'c', u'f', u'g', u'p', u't'] and c[1] in [u'l', u'r'] and c != u"dl") or c in [u'dr', u'kr', u'll', u'rr'] else False


def guegui(c):
	if len(c) < 3: return False
	return True if (c[0:1] == u'g' and c[1] == u'u' and c[2] in [u'e', u'i']) else False


def diptongo(trozo):
	if len(trozo) < 2: return False
	if trozo[0:2] in [u'ai', u'au', u'ei', u'eu', u'io', u'ou', u'ia', u'ua', u'ie', u'ue', u'oi', u'uo', u'ui', u'iu']: return True
	if len(trozo) == 2 and trozo in [u'ay', u'ey', u'oy']: return True
	return False


def dieresis(trozo):
	if len(trozo) < 2: return False
	return True if trozo[0:2] in [u'üe', u'üi'] else False


def diptongo_con_h(trozo):
	if len(trozo) < 3: return False
	t = trozo[0:3]

	if t[1] == u'h':
		if len(trozo) > 3 and trozo[2:4] == u'ue':
			return False
		else:
			t = t.replace(u'h', u'')
	else:
		return False

	return diptongo(t)


def triptongo(trozo):
	if len(trozo) < 3: return False
	return True if trozo[0:3] in [u'iai', u'iei', u'uai', u'uei', u'uau', u'iau', u'iái', u'iéi', u'uái', u'uéi', u'uáu', u'iáu', u'uay', u'uey'] else False


def coda(trozo):
	l = len(trozo)
	if l < 1: return 0 # fin de palabra, no quedan letras
	if l < 2 and consonante(trozo[0]): return 1 # V+C fin de palabra, se añade
	if l > 1 and ataque_complejo(trozo[0:2]): return 0 # V +C+C inseparables, a la siguiente
	if l > 1 and consonante(trozo[0]) and vocal([1]): return 0 # V +C+V, irá con la siguiente sílaba
	if l > 2 and consonante(trozo[0]) and consonante(trozo[1]) and vocal(trozo[2]): return 1 # V+C +C+V
	if l > 3 and consonante(trozo[0]) and ataque_complejo(trozo[1:3]) and vocal(trozo[3]): return 1 # V+C +C+C+V
	if l > 3 and consonante(trozo[0]) and consonante(trozo[1]) and consonante(trozo[2]) and vocal(trozo[3]): return 2 # V+C+C +C+V
	if l > 3 and consonante(trozo[0]) and consonante(trozo[1]) and consonante(trozo[2]) and consonante(trozo[3]): return 2 # V+C+C +C+C+V
	return 0


def minusculas(texto):
	ret = ""
	mapeo = {u'Á': u'á', u'É': u'é', u'Í': u'í', u'Ó': u'ó', u'Ú': u'ú', u'Ü': u'ü', u'Ñ': u'ñ'}
	for letra in texto:
		if letra in mapeo:
			ret += letra.replace(letra, mapeo[letra])
		else:
			ret += letra.lower()
	return ret


if __name__ == '__main__':
	palabras = ""
	palabras += u"guiais"
	#palabras += u"onomatopeya"
	#palabras += u"hipopotomonstrosesquipedaliofobia"
	#palabras += u"aorta héroe almohada línea mediterráneo cohete alcohol "
	#palabras += u"deshora deshielo "
	#palabras += u"terapéutica saúco sabía día toalla "
	#palabras += u"pasguato "
	#palabras += u"paraguas "
	#palabras += u"ambigüedad pingüino cigüeña "
	#palabras += u"cacahuete vihuela "
	#palabras += u"país baúl reí reúne filosofía río ríe oí noúmeno púa acentúo maíz "
	#palabras += u"teatro caoba saeta zoólogo "
	#palabras += u"albergue guadalupe abrigo guia guiso "
	#palabras += u"españa piña "
	#palabras += u"maría ahuyentar aereo jaula "
	#palabras += u"cumple transporte une componer aprender "
	#palabras += u"hola perro"
	#for palabra in palabras.split(" "):
	#	print palabra, " = ", " - ".join(silabas(palabra))
	#	print
	#	time.sleep(2)
	print silabas(palabras.replace(" ", ""))
