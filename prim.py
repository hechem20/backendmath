
from sympy import *
import string
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import io
import sys
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def ind(u, ch, m):
    i = m
    k = 0
    while (k == 0) and i < len(u):
        if u[i] == ch:
            k = 1
        i = i + 1
    if k == 1:
        return i - 1
    else:
        return -1

def div(m):
    j = ind(m, '/', 0)
    k = 0
    while j != -1 and k == 0:
        c = j
        if m[:j].count('(') == m[:j].count(')'):
            k = 1
        j = ind(m, '/', j + 1)
    if k == 1:
        if (vrex(m[:c]) == 0 and vrex(m[c:]) == 0) or (vret(m[:c]) == 0 and vret(m[c:]) == 0):
            return c
        else:
            return 0
    else:
        return 0

def prod(m):
    j = ind(m, '*', 0)
    l = []
    while j != -1:
        if m[:j].count('(') == m[:j].count(')'):
            l.append(j)
        j = ind(m, '*', j + 1)
    if len(l) > 0 and div(m) == 0:
        if (vrex(m[:l[len(l) - 1]]) == 0 and vrex(m[l[len(l) - 1]:]) == 0) or (vret(m[:l[len(l) - 1]]) == 0 and vret(m[l[len(l) - 1]:]) == 0):
            return l[len(l) - 1]
        else:
            return 0
    else:
        return 0

def deri(n):
    k = 0
    for i in range(1, len(n)):
        if (n[i] == '+' or n[i] == '-') and (n[:i].count(')') == n[:i].count('(')):
            k = k + 1
    return k

def suit(n, pos):
    i = pos + 1
    k = 0
    while k >= 0:
        if (n[i] == '('):
            k = k + 1
        if (n[i] == ')'):
            k = k - 1
        i = i + 1
    return i - 1

def divsio(u):
    i = ind(u, '/', 0)
    k = 0
    while i != -1 and k == 0:
        c = i
        if u[i] == '/' and u[:i].count(')') == u[:i].count('('):
            k = 1
        i = ind(u, '/', i + 1)
    if k == 1:
        return c
    else:
        return -1

def derivp(n):
    l = []
    for i in range(1, len(n)):
        if (n[i] == '+' or n[i] == '-') and (n[:i].count(')') == n[:i].count('(')):
            l.append(i)
    if l == [] or l[0] != 0:
        l.insert(0, 0)
    l.append(len(n))
    return l

def nb0(u):
    try:
        a = float(u)
    except:
        a = 0
    return a

def nb1(u):
    j = ind(u, '*', 0)
    if j != -1 and u[:j].count(')') == u[:j].count('(') and nb0(sympify(u[:j])) != 0:
        return u[:j]
    elif nb0(sympify(u)) != 0:
        return u
    else:
        if u[0] == '-':
            return -1
        else:
            return 1

def chnb(u):
    f = divsio(u)
    if f != -1:
        if u[f + 1] == '(' and suit(u, f + 1) == len(u) - 1:
            return sympify(str(nb1(u[:f])) + '/' + str(nb1(u[f + 2:len(u) - 1])))
        else:
            return sympify(str(nb1(u[:f])) + '/' + str(nb1(u[f + 1:])))
    else:
        return sympify(nb1(u))

def conv(m):
    if deri(m) == 0 and 'Integ' not in m and 'lam' not in m:
        if div(m) != 0:
            return [0, div(m), chnb(m)]
        elif prod(m) != 0:
            return [1, prod(m), chnb(m)]
        else:
            i = 0
            k = 0
            while k == 0:
                if m[i] == '(' and (vrex(m[i:suit(m, i)]) == 0 or vret(m[i:suit(m, i)]) == 0) and m[i - 1] != '/':
                    k = 1
                if (m[i] == 'x' and (i - 1 == -1 or m[i - 1] != 'e')) or (m[i] == 't' and (i - 1 == -1 or (m[i - 1] != 'r' and m[i - 1] != 'a'))):
                    k = 1
                i = i + 1
            i = i - 1
            if (m[i] == 'x' and (i - 1 == -1 or m[i - 1] != 'e')) or (m[i] == 't' and (i - 1 == -1 or m[i - 1] != 'r' or m[i - 1] != 'a')):
                return [-1]
            elif suit(m, i) == len(m) - 1 or m[suit(m, i) + 1:suit(m, i) + 3] != '**' and '/' not in m[:i]:
                return [2, i, chnb(m)]
            elif m[suit(m, i) + 1:suit(m, i) + 3] == '**' and '/' not in m[:i]:
                if m[suit(m, i) + 3] != '(':
                    return [3, i, chnb(m)]
                else:
                    return [31, i, chnb(m)]
            elif '/' in m[:i]:
                q = i
                while m[q] != '/' and m[q] != '*':
                    q = q - 1
                if m[suit(m, i) + 1:suit(m, i) + 3] == '**':
                    return [4, q, chnb(m)]
                else:
                    return [41, q, chnb(m)]
            elif m[i - 4:i + 1] == 'sqrt(' and '/' not in m[:i]:
                return [5, i, chnb(m)]
    else:
        return []

def vrex(n):
    j = ind(n, 'x', 0)
    k = 0
    while j != -1 and k == 0:
        if j + 1 == len(n) or n[j + 1] != 'p':
            k = 1
        j = ind(n, 'x', j + 1)
    if k == 1:
        return 0
    else:
        return 1

def pp(u):
    x = Symbol('x')
    t = Symbol('t')
    if vrex(u) == 0:
        return x
    else:
        return t

def vret(n):
    i = 0
    k = 0
    while i < len(n) and k == 0:
        if n[i] == 't' and (i == 0 or not (n[i - 1].isalpha())):
            k = 1
        i = i + 1
    if k == 1:
        return 0
    else:
        return 1

def inclus(u):
    i = ind(u, '(', 0)
    k = 0
    while i != -1 and k == 0:
        c = i
        if 'x' in u[i:suit(u, i)] or 't' in u[i:suit(u, i)]:
            k = 1
        i = ind(u, '(', i + 1)
    return c

def cont(m, n, x):
    x = Symbol(str(x))
    m = str(m)
    j = inclus(m)
    if n == 0:
        sh = str(diff(sympify(m[m.index('n') + 2:m.rindex(')')]), x))
        ch = '(' + sh + ')/(1+(' + m[m.index('n') + 2:m.rindex(')')] + ')**2)'
    elif n == 1:
        sh = str(diff(sympify(m[m.index('n') + 2:m.rindex(')')]), x))
        ch = '(' + sh + ')/sqrt(1-(' + m[m.index('n') + 2:m.rindex(')')] + ')**2)'
    elif n == 2:
        sh = str(diff(sympify('-' + m[m.index('n') + 2:m.rindex(')')]), x))
        ch = '(' + sh + ')/sqrt(1-(' + m[m.index('n') + 2:m.rindex(')')] + ')**2)'
    elif n == 3:
        sh = str(diff(sympify(m[j + 1:suit(m, j)]), x))
        ch = '(' + sh + ')/sqrt(' + m[j + 1:suit(m, j)] + ')'
    elif n == 4:
        sh = str(diff(sympify(m[j + 1:suit(m, j)]), x))
        ch = '(' + sh + ')*exp(' + m[j + 1:suit(m, j)] + ')'
    elif n == 5:
        sh = str(diff(sympify(m[j + 1:suit(m, j)]), x))
        ch = '(' + sh + ')/(' + m[j + 1:suit(m, j)] + ')'
    elif n == 6:
        sh = str(diff(sympify(m[j + 1:suit(m, j)]), x))
        ch = '(' + sh + ')*sin(' + m[j + 1:suit(m, j)] + ')'
    elif n == 7:
        sh = str(diff(sympify(m[j + 1:suit(m, j)]), x))
        ch = '(' + sh + ')*cos(' + m[j + 1:suit(m, j)] + ')'
    return sympify(ch)

def conts(m, n):
    x = Symbol('x')
    t = Symbol('t')
    if vrex(str(m)) == 0:
        return cont(m, n, x)
    else:
        return cont(m, n, t)

def ordonne(u):
    sh = ""
    ch = ""
    ah = ""
    d = []
    c = []
    d = derivp(u)
    for i in range(0, len(d) - 1):
        c = conv(str(integrate(sympify(u[d[i]:d[i + 1]]), pp(u[d[i]:d[i + 1]]))))
        if len(c) == 0:
            ah = ah + u[d[i]:d[i + 1]]
        else:
            sh = sh + u[d[i]:d[i + 1]]
    if len(ah) != 0:
        if ah[0] == '+' or ah[0] == '-':
            ch = sh + ah
        else:
            ch = sh + '+' + ah
    else:
        ch = u
    return ch


def primitive(s,fh):
    x=Symbol('x')
    t=Symbol('t')
    u=Symbol('u')
    u1=Symbol('u1')
    v=Symbol('v')
    v1=Symbol('v1')
    l=[]
    c=[]
    i=0
    y=0
    ch=""
    if '||' in s:
        s=s[s.index('|')+2:]
    s=ordonne(s)
    l=derivp(s)
    while i<len(l)-1 and y==0:
        if (s[l[i]]=='+' or s[l[i]]=='-'):
            tc=s[l[i]+1:l[i+1]]
        else:
            tc=s[l[i]:l[i+1]]
        n=sympify(tc)
        if vret(str(n))==0:
            m=integrate(n,t)
        elif vrex(str(n))==0:
            m=integrate(n,x)
        else:
            if vret(s)==0:
                m=integrate(n,t)
            else:
                m=integrate(n,x)
        if ver1(str(m),'sqrt(',0)==0:
            m=simplify(m)
        else:
            m=expand(m)
        
        f=str(m)
        c=conv(f)
        if len(c)>0 and (c[0]==0 or c[0]==1):
            f1=str(sympify(f+'*'+'(1/'+str(c[2])+')'))
            c1=conv(f1)
        if len(c)!=0 or 'integr' in str(m) or 'lampda' in str(m) or '$' in str(m):
            if c[0]==0:
                print("   📐 Forme: (u'·v - v'·u)/v²")
                print(f"      u = {f1[:c1[1]]}, v = {f1[c1[1]+1:]}")
                print(f"   ∫ {tc} d{pp(str(n))} = {m}")
            elif c[0]==1:
                print("   📐 Forme: u'·v + v'·u")
                print(f"      u = {f1[:c1[1]]}, v = {f1[c1[1]+1:]}")
                print(f"   ∫ {tc} d{pp(str(n))} = {m}")
            elif c[0]==2:
                if f[c[1]-1]=='t':
                    print("   📐 Forme: u'/√u  →  ∫ u'/√u du = 2√u")
                    print(f"      u = {f[c[1]+1:suit(f,c[1])]}")
                    print(f"   ∫ {tc} d{pp(str(n))} = {m}")
                elif f[c[1]-1]=='p':
                    print("   📐 Forme: u'·exp(u)  →  ∫ u'·e^u du = e^u")
                    print(f"      u = {f[c[1]+1:suit(f,c[1])]}")
                    print(f"   ∫ {tc} d{pp(str(n))} = {m}")
                elif f[c[1]-1]=='g':
                    print("   📐 Forme: u'/u  →  ∫ u'/u du = ln|u|")
                    print(f"      u = {f[c[1]+1:suit(f,c[1])]}")
                    print(f"   ∫ {tc} d{pp(str(n))} = {m}")
                elif f[c[1]-1]=='s' and (c[1]-3==0 or f[c[1]-4]!='a'):
                    print("   📐 Forme: u'·sin(u)  →  ∫ u'·sin(u) du = -cos(u)")
                    print(f"      u = {f[c[1]+1:suit(f,c[1])]}")
                    print(f"   ∫ {tc} d{pp(str(n))} = {m}")
                elif f[c[1]-1]=='n' and (c[1]-3==0 or f[c[1]-4]!='a'):
                    print("   📐 Forme: u'·cos(u)  →  ∫ u'·cos(u) du = sin(u)")
                    print(f"      u = {f[c[1]+1:suit(f,c[1])]}")
                    print(f"   ∫ {tc} d{pp(str(n))} = {m}")
                elif f[c[1]-1]=='n' and f[c[1]-2]=='a':
                    print("   📐 Forme: u'/(1+u²)  →  ∫ u'/(1+u²) du = arctan(u)")
                    print(f"      u = {f[c[1]+1:suit(f,c[1])]}")
                    print(f"   ∫ {tc} d{pp(str(n))} = {m}")
                elif f[c[1]-1]=='n' and f[c[1]-4]=='a':
                    print("   📐 Forme: u'/√(1-u²)  →  ∫ u'/√(1-u²) du = arcsin(u)")
                    print(f"      u = {f[c[1]+1:suit(f,c[1])]}")
                    print(f"   ∫ {tc} d{pp(str(n))} = {m}")
                elif f[c[1]-1]=='s' and f[c[1]-4]=='a':
                    print("   📐 Forme: -u'/√(1-u²)  →  ∫ -u'/√(1-u²) du = arccos(u)")
                    print(f"      u = {f[c[1]+1:suit(f,c[1])]}")
                    print(f"   ∫ {tc} d{pp(str(n))} = {m}")
            elif c[0]==31:
                print("   📐 Forme: u'·√u  →  ∫ u'·√u du = (2/3)·u^(3/2)")
                q=f[:c[1]].find('*')
                q=q+1
                print(f"      u = {f[q:f.rfind('**')]}")
                print(f"   ∫ {tc} d{pp(str(n))} = {m}")
            elif c[0]==-1:
                print(f"   ∫ {tc} d{pp(str(n))} = {m}")
            else:
                print(f"   ∫ {tc} d{pp(str(n))} = {m}")
        else:
            if expver(tc,['exp(','cos('])==0:
                tc=cosexp(tc)
            elif expver(tc,['exp(','sin('])==0:
                tc=sinexp(tc)
            elif expver(tc,[-1,'exp('])==0:
                tc=xnexp(tc)
            elif expver(tc,[-1,'exp(','cos('])==0:
                tc=xnexpcos(tc)
            elif expver(tc,[-1,'exp(','sin('])==0:
                tc=xnexpsin(tc)
            elif expver(tc,[-1,'cos('])==0:
                tc=xncos(tc)
            elif expver(tc,[-1,'sin('])==0:
                tc=xnsin(tc)
            elif expver(tc,['cos(','sin('])==0:
                tc=sincos(tc)
            elif expver(tc,['sin('])==0 and ('/' not in tc or nb0(tc[tc.index('/')+1:])!=0):
                tc=sins(tc)
            elif expver(tc,['cos('])==0 and ('/' not in tc or nb0(tc[tc.index('/')+1:])!=0):
                tc=coss(tc)
            else:
                prim(tc,fh)
        i=i+1
    print("=",simplify(fh))
    return

# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS SUPPLÉMENTAIRES (à conserver telles quelles)
# ═══════════════════════════════════════════════════════════════════════════════

def iden(m, n):
    ch = ""
    dict = {}
    for i in n.keys():
        dict[str(i)] = n[i]
    for i in range(0, len(m)):
        if m[i] in dict.keys():
            ch = ch + str(dict[(m[i])])
        else:
            ch = ch + m[i]
    ch = str(sympify(ch))
    print(ch)
    return ch

def tran(m):
    x = Symbol('x')
    t = Symbol('t')
    m = simplify(sympify(m))
    m = ratsimp(m)
    m = together(m)
    print(m)
    m = str(m)
    j = str(expand(sympify(m[:m.index('/')])))
    n = '(' + sum(j) + ')'
    n = n + m[m.index('/'):]
    return n

def simp(u):
    d = []
    d.append(-1)
    for i in range(0, len(u)):
        if u[i] == '*' and u[i - 1] != '*' and u[i + 1] != '*' and u[:i].count('(') == u[:i].count(')') and (vrex(u[d[len(d) - 1] + 1:i]) == 0 or vret(u[d[len(d) - 1] + 1:i]) == 0):
            d.append(i)
    d.append(len(u))
    return d

def fact(u):
    sh = ""
    l = []
    x = Symbol('x')
    t = Symbol('t')
    dict = roots(sympify(u))
    s = str(sympify(u))
    if s[0] != 'x' and s[0] != 't' and s[0] != '-':
        sh = sh + s[0] + '*'
    if s[0] == '-':
        sh = sh + '-1*'
    for i in dict.keys():
        if 'x' in u:
            sh = sh + '(x-(' + str(i) + '))**' + str(dict[i]) + '*'
        else:
            sh = sh + '(t-(' + str(i) + '))**' + str(dict[i]) + '*'
    sh = sh[:len(sh) - 1]
    m = str(sympify(sh))
    l = simp(m)
    j = 0
    ch = ""
    while j < len(l) - 1:
        if 'I' in m[l[j] + 1:l[j + 1]]:
            d = str(expand(sympify(m[l[j] + 1:l[j + 2]])))
            ch = ch + '(' + d + ')*'
            j = j + 2
        else:
            ch = ch + m[l[j] + 1:l[j + 1]] + '*'
            j = j + 1
    ch = ch[:len(ch) - 1]
    ch = str(sympify(ch))
    if degree(sympify(u)) > 2 or (degree(sympify(u)) == 2 and discriminant(sympify(u)) > 0):
        print(sympify(u),"=", sympify(ch))
    return ch

def deg(u):
    sh = string.ascii_lowercase
    x = Symbol('x')
    t = Symbol('t')
    ch = ""
    j = degree(sympify(u[:u.index('/')])) - degree(sympify(u[u.index('/') + 1:]))
    if j >= 0:
        print("degree of the numerator greater than or equal to that of the denominator")
        for i in range(0, j + 1):
            if 'x' in u:
                ch = ch + sh[i] + '*x**' + str(i) + '+'
            else:
                ch = ch + sh[i] + '*t**' + str(i) + '+'
        ch = ch + '('
        for k in range(0, degree(sympify(u[u.index('/') + 1:]))):
            if 'x' in u:
                ch = ch + sh[j + k + 1] + '*x**' + str(k) + '+'
            else:
                ch = ch + sh[j + k + 1] + '*t**' + str(k) + '+'
        ch = ch[:len(ch) - 1]
        ch = ch + ')'
        ch = ch + u[u.index('/'):]
        ch = str(sympify(ch))
        print(sympify(u), "=", sympify(ch))
        ah = tran(ch)
        print("=", ah)
        if 'x' in ah:
            ch = iden(ch, cherche(sympify(ah[:ah.index('/')]), sympify(u[:u.index('/')])))
        else:
            ch = iden(ch, cherche(sympify(ah[:ah.index('/')]), sympify(u[:u.index('/')])))
        print("=", ch)
    else:
        ch = u
    return ch

def fac(sh):
    d = []
    if '/' not in sh and len(sh) > 6 and sh[len(sh) - 6:len(sh) - 4] == '**' and sh[len(sh) - 4] == '(':
        sh = '1/' + sh[:len(sh) - 4] + sh[len(sh) - 2]
    if sh[sh.index('/') + 1] == '(':
        ch = sh[:sh.index('/') + 2]
    else:
        ch = sh[:sh.index('/') + 1]
    if sh[sh.index('/') + 1] == '(' and deri(sh[sh.index('/') + 2:suit(sh, sh.index('/') + 1)]) == 0:
        l = simp(sh[sh.index('/') + 2:len(sh) - 1])
        s = 1
    else:
        l = simp(sh[sh.index('/') + 1:len(sh)])
        s = 0
    for i in range(0, len(l)):
        l[i] = l[i] + len(sh[:sh.index('/') + 1]) + s
    for j in range(0, len(l) - 1):
        if sh[l[j + 1] - 3:l[j + 1] - 1] == '**':
            k = 3
        else:
            k = 0
        m = fact(sh[l[j] + 1:l[j + 1] - k])
        if k == 3:
            d = simp(m)
            n = ""
            for i in range(0, len(d) - 1):
                n = n + '(' + m[d[i] + 1:d[i + 1]] + ')**' + sh[l[j + 1] - 1] + '*'
            m = n
            m = m[:len(m) - 1]
        ch = ch + '(' + m + ')*'
    ch = ch[:len(ch) - 1]
    if sh[sh.index('/') + 1] == '(':
        ch = ch + ')'
    ch = str(sympify(ch))
    print(ch)
    return ch

def polydiv(ch):
    ah = string.ascii_lowercase
    x = Symbol('x')
    t = Symbol('t')
    ch = fac(ch)
    sh = ""
    qh = ""
    if '/' not in ch and len(ch) > 6 and ch[len(ch) - 6:len(ch) - 4] == '**' and ch[len(ch) - 4] == '(':
        ch = '1/' + ch[:len(ch) - 4] + ch[len(ch) - 2]
    if ch[ch.index('/') + 1] == '(' and deri(ch[ch.index('/') + 2:suit(ch, ch.index('/') + 1)]) == 0:
        l = simp(ch[ch.index('/') + 2:len(ch) - 1])
        s = 1
    else:
        l = simp(ch[ch.index('/') + 1:len(ch)])
        s = 0
    for i in range(0, len(l)):
        l[i] = l[i] + len(ch[:ch.index('/') + 1]) + s
    q = 0
    if len(l) == 2 and ch[len(ch) - 3:len(ch) - 1] == '**' and degree(sympify(ch[:ch.index('/')])) >= degree(sympify(ch[ch.index('/') + 1:len(ch) - 3])):
        q = 1
        l[0] = ch.index('/')
        l[1] = len(ch)
    c = 0
    if len(l) > 2 or q == 1:
        for i in range(0, len(l) - 1):
            if ch[l[i + 1] - 3:l[i + 1] - 1] == '**':
                tp = int(ch[l[i + 1] - 1])
                for j in range(1, tp + 1):
                    for k in range(0, degree(sympify(ch[l[i] + 1:l[i + 1] - 3]))):
                        if 'x' in ch:
                            qh = qh + ah[c] + '*x**' + str(k) + '+'
                        else:
                            qh = qh + ah[c] + '*t**' + str(k) + '+'
                        c = c + 1
                    qh = '(' + qh[:len(qh) - 1] + ')'
                    sh = sh + qh + '/(' + ch[l[i] + 1:l[i + 1] - 1] + str(j) + ')+'
                    qh = ""
            else:
                sh = sh + '('
                if 'x' in ch:
                    fm = degree(sympify(ch[l[i] + 1:l[i + 1]]), x)
                else:
                    fm = degree(sympify(ch[l[i] + 1:l[i + 1]]), t)
                for s in range(0, fm):
                    if 'x' in ch:
                        sh = sh + ah[c] + '*x**' + str(s) + '+'
                    else:
                        sh = sh + ah[c] + '*t**' + str(s) + '+'
                    c = c + 1
                sh = sh[:len(sh) - 1]
                sh = sh + ')/(' + ch[l[i] + 1:l[i + 1]] + ')+'
        sh = sh[:len(sh) - 1]
        sh = str(sympify(sh))
        print(ch, "=", sh)
        ah = tran(sh)
        print("=", ah)
        sh = iden(sh, cherche(sympify(ah[:ah.index('/')]), sympify(ch[:ch.index('/')])))
        print("=", sh)
    else:
        sh = ch
    return sh

def sum(m):
    x = Symbol('x')
    t = Symbol('t')
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    n = sympify(m)
    if 'x' in m:
        j = degree(n, x)
    else:
        j = degree(n, t)
    if 'x' in m:
        y = poly(n, x)
    else:
        y = poly(n, t)
    c = y.all_coeffs()
    ch = ""
    for i in range(0, len(c)):
        if 'x' in m:
            ch = ch + '(' + str(c[i]) + ')*x**(' + str(j) + '-' + str(i) + ')+'
        else:
            ch = ch + '(' + str(c[i]) + ')*t**(' + str(j) + '-' + str(i) + ')+'
    ch = ch[:len(ch) - 1]
    ch = str(sympify(ch))
    return ch

def cherche(u, v):
    c = []
    d = []
    s = []
    x = Symbol('x')
    t = Symbol('t')
    if 'x' in str(u):
        ta = degree(u, x)
        tb = degree(v, x)
    else:
        ta = degree(u, t)
        tb = degree(v, t)
    if ta > tb:
        for i in range(0, ta - tb):
            d.append(0)
    if 'x' in str(u):
        a = poly(u, x)
        b = poly(v, x)
    else:
        a = poly(u, t)
        b = poly(v, t)
    c = a.all_coeffs()
    d = d + b.all_coeffs()
    for i in range(0, len(c)):
        print(c[i], "=", d[i])
        s.append(Eq(c[i], d[i]))  # ✅ CORRECT
    print(solve(s))
    return solve(s)

def div3(u):
    x = Symbol('x')
    t = Symbol('t')
    c1 = []
    c = []
    d = []
    if '/' not in u and len(u) > 6 and u[len(u) - 6:len(u) - 4] == '**' and u[len(u) - 4] == '(':
        u = '1/' + u[:len(u) - 4] + u[len(u) - 2]
    f = divsio(u)
    sh = ""
    if f != -1 and u[len(u) - 3:len(u) - 1] == '**' and degree(sympify(u[f + 1:len(u) - 3])) == 2:
        if vrex(u) == 0:
            m = integrate(sympify(u), x)
        else:
            m = integrate(sympify(u), t)
        if deri(str(m)) != 0:
            a = poly(sympify(u[f + 1:len(u) - 3]))
            c = a.all_coeffs()
            ch = u
            if degree(sympify(u[:f])) == 1:
                b = poly(sympify(u[:f]))
                d = b.all_coeffs()
                sh = sympify((d[0] / 2 * c[0]) * (diff(sympify(u[f + 1:len(u) - 3]))) / (sympify(u[f + 1:])) + (d[1] - (c[1] * d[0]) / (2 * c[0])) / (sympify(u[f + 1:])))
                print("=", sh)
                sh = sympify((d[0] / 2 * c[0]) * (diff(sympify(u[f + 1:len(u) - 3]))) / (sympify(u[f + 1:])))
                ch = str((d[1] - (c[1] * d[0]) / (2 * c[0]))) + '/' + str((sympify(u[f + 1:])))
            a = poly(sympify(u[f + 1:len(u) - 3]))
            c1 = a.all_coeffs()
            j = c1[1] ** 2 / (4 * c1[0])
            i = c1[2] - j
            if i > 0:
                k = '(1/' + str(i) + ')*(x+' + str(sqrt(j)) + ')'
                ch = ch[:ch.index('/') + 1] + '(' + str(i) + '*(' + k + '**2+1))'
                ch = str(sympify(ch))
                print("=", ch)
                print("by change of variable :", sympify(k + '*' + str(sqrt(i))), "=", tan(t), ";dx=", (1 + tan(t) ** 2) * sqrt(i), "dt")
                ch = ch[:ch.index('/')] + '*cos(t)**' + str(sympify('2*(' + u[len(u) - 1] + '-1)')) + '/' + str(sqrt(i))
                print(sympify(ch))
                ch = str(sh) + '+' + ch
                return str(sympify(ch))
            else:
                return u
        else:
            return u
    else:
        return u

def div2(u):
    x = Symbol('x')
    t = Symbol('t')
    m = ""
    c = []
    d = []
    f = divsio(u)
    if f != -1 and degree(sympify(u[f + 1:])) == 2 and degree(sympify(u[:f])) == 1:
        if u[f + 1:].count('x') == 2 or u[f + 1:].count('t') == 2:
            a = poly(sympify(u[f + 1:]))
            b = poly(sympify(u[:f]))
            c = a.all_coeffs()
            d = b.all_coeffs()
            m = sympify((d[0] / 2 * c[0]) * (diff(sympify(u[f + 1:]))) / (sympify(u[f + 1:])) + (d[1] - (c[1] * d[0]) / (2 * c[0])) / (sympify(u[f + 1:])))
            print(sympify(u), "=", m)
        else:
            i = 1
            k = 0
            while k == 0 and i < len(u[:f]):
                if u[i] == '+' or u[i] == '-':
                    k = 1
                i = i + 1
            if k == 1:
                m = sympify(u[:i - 1] + ')/' + u[f + 1:] + '+(' + u[i - 1:f] + '/' + u[f + 1:])
                print(sympify(u), "=", m)
            else:
                m = sympify(u)
    else:
        m = sympify(u)
    return str(m)

def supp(ch):
    s = ""
    for i in range(0, len(ch)):
        if ch[i] != ' ':
            s = s + ch[i]
    return s

def polys(u):
    ch = ""
    d = []
    c = []
    u = deg(u)
    u = str(sympify(u))
    d = derivp(u)
    k = 0
    i = 0
    while k == 0 and i < len(d) - 1:
        if divsio(u[d[i]:d[i + 1]]) != -1 and u[d[i] + divsio(u[d[i]:d[i + 1]]) + 1] == '(':
            k = 1
        i = i + 1
    i = i - 1
    sh = u[d[i]:d[i + 1]]
    sh = polydiv(sh)
    s = u[:d[i]] + '+' + u[d[i + 1]:] + '+' + sh
    s = str(sympify(s))
    c = derivp(s)
    for i in range(0, len(c) - 1):
        k = div2(s[c[i]:c[i + 1]])
        ch = ch + '+' + k
    ch = str(sympify(ch))
    c = derivp(ch)
    ah = ""
    for j in range(0, len(c) - 1):
        z = div3(ch[c[j]:c[j + 1]])
        ah = ah + '+' + z
    print("=", sympify(ah))
    return str(sympify(ah))

def racine0(u):
    ah = ""
    c = []
    j = u.index('t')
    a = poly(sympify(u[j + 2:suit(u, j + 2)]))
    c = a.all_coeffs()
    a1 = str(sympify('sqrt(-' + str(c[0]) + ')'))
    b = str(sympify(str(c[1]) + '/(2*' + a1 + ')'))
    c = str(sympify(str(c[2]) + '+' + b + '**2'))
    ch = sympify('sqrt(' + c + '-(' + a1 + '*x-' + b + ')**2)')
    ch = u[:u.index('/') + 1] + str(ch)
    print(u, "=", ch)
    ch = u[:u.index('/') + 1] + str(sympify('sqrt(' + '(' + c + ')' + ')*sqrt(1-((' + a1 + '*x-' + b + ')/sqrt(' + c + '))**2)'))
    print("=", ch)
    ah = simplify(sympify(u[:u.index('/')] + '*asin(' + '(' + a1 + '*x-' + b + ')/sqrt(' + c + '))*(1/(' + a1 + '))'))
    print("=", ah)
    return str(ah)

def racine1(u):
    if degree(sympify(u[:u.index('/')])) == 1 and degree(sympify(u[u.index('t') + 1:])) == 2:
        a = poly(sympify(u[u.index('t') + 1:]))
        b = poly(sympify(u[:u.index('/')]))
        c = a.all_coeffs()
        d = b.all_coeffs()
        m = sympify((d[0] / 2 * c[0]) * (diff(sympify(u[u.index('t') + 1:]))) / (sympify(u[u.index('/') + 1:])) + (d[1] - (c[1] * d[0]) / (2 * c[0])) / (sympify(u[u.index('/') + 1:])))
        print(sympify(u), "=", m)
    else:
        m = sympify(u)
    return str(m)

def racine2(u):
    if len(u[:u.index('s')]) != 0 and degree(sympify(u[:u.index('s') - 1])) == 1 and degree(sympify(u[u.index('t') + 1:])) == 2:
        a = poly(sympify(u[u.index('t') + 1:]))
        b = poly(sympify(u[:u.index('s') - 1]))
        c = a.all_coeffs()
        d = b.all_coeffs()
        m = sympify((d[0] / 2 * c[0]) * (diff(sympify(u[u.index('t') + 1:]))) * sympify(u[u.index('s'):]) + (d[1] - (c[1] * d[0]) / 2 * (c[0])) * sympify(u[u.index('s'):]))
        print(sympify(u), "=", m)
    else:
        m = sympify(u)
    return str(m)

def cosexp(u):
    x = Symbol('x')
    t = Symbol('t')
    y = chnb(u)
    if y != 1:
        u1 = u
        u = str(sympify(u + '*1/' + str(y)))
        if vrex(u) == 0:
            print(Integral(sympify(u1), x), "=", y * Integral(sympify(u), x))
        else:
            print(Integral(sympify(u1), t), "=", y * Integral(sympify(u), t))
    a = poly(sympify(u[u.index('s') + 2:suit(u, u.index('s') + 1)]))
    b = poly(sympify(u[u.index('p') + 2:suit(u, u.index('p') + 1)]))
    c = a.all_coeffs()
    d = b.all_coeffs()
    if u[suit(u, u.index('s') + 1) + 1:suit(u, u.index('s') + 1) + 3] == '**':
        c[0] = c[0] * int(u[suit(u, u.index('s') + 1) + 3])
    if vrex(u) == 0:
        f = sympify('exp((' + str(d[0]) + '+' + str(I * c[0]) + ')*x +' + str(I * c[1]) + '+' + str(d[1]) + ')')
    else:
        f = sympify('exp((' + str(d[0]) + '+' + str(I * c[0]) + ')*t +' + str(I * c[1]) + '+' + str(d[1]) + ')')
    print("real(|", f, "|)")
    print('1/(' + str(sympify(str(d[0]) + '+' + str(I * c[0]))) + ')*' + str(f))
    print('(' + str(sympify(str(d[0]) + '-' + str(I * c[0]))) + ')/((' + str(sympify(str(d[0]) + '+' + str(I * c[0]))) + ')*(' + str(sympify(str(d[0]) + '-' + str(I * c[0]))) + '))*' + str(f))
    if vrex(u) == 0:
        j = integrate(f, x)
    else:
        j = integrate(f, t)
    print("real(", simplify(j), ")")
    print("real(", expand(j), ")")
    s = sympify(u + '*' + str(y))
    if vrex(u) == 0:
        s = integrate(s, x)
    else:
        s = integrate(s, t)
    print(s)
    return str(s)

def sinexp(u):
    x = Symbol('x')
    t = Symbol('t')
    y = chnb(u)
    if y != 1:
        u1 = u
        u = str(sympify(u + '*1/' + str(y)))
        if vrex(u) == 0:
            print(Integral(sympify(u1), x), "=", y * Integral(sympify(u), x))
        else:
            print(Integral(sympify(u1), t), "=", y * Integral(sympify(u), t))
    a = poly(sympify(u[u.index('n') + 2:suit(u, u.index('n') + 1)]))
    b = poly(sympify(u[u.index('p') + 2:suit(u, u.index('p') + 1)]))
    c = a.all_coeffs()
    d = b.all_coeffs()
    if u[suit(u, u.index('n') + 1) + 1:suit(u, u.index('n') + 1) + 3] == '**':
        c[0] = c[0] * int(u[suit(u, u.index('n') + 1) + 3])
    if vrex(u) == 0:
        f = sympify('exp((' + str(d[0]) + '+' + str(I * c[0]) + ')*x +' + str(I * c[1]) + '+' + str(d[1]) + ')')
    else:
        f = sympify('exp((' + str(d[0]) + '+' + str(I * c[0]) + ')*t +' + str(I * c[1]) + '+' + str(d[1]) + ')')
    print("im(|", f, "|)")
    print('1/(' + str(sympify(str(d[0]) + '+' + str(I * c[0]))) + ')*' + str(f))
    print('(' + str(sympify(str(d[0]) + '-' + str(I * c[0]))) + ')/((' + str(sympify(str(d[0]) + '+' + str(I * c[0]))) + ')*(' + str(sympify(str(d[0]) + '-' + str(I * c[0]))) + '))*' + str(f))
    if vrex(u) == 0:
        j = integrate(f, x)
    else:
        j = integrate(f, t)
    print("im(", simplify(j), ")")
    print("im(", expand(j), ")")
    s = sympify(u + '*' + str(y))
    if vrex(u) == 0:
        s = integrate(f, x)
    else:
        s = integrate(f, t)
    print(s)
    return str(s)

def parparti(v, u, p):
    if len(u) > 3 and u[:2] == 'ex':
        sh = 'ex'
    else:
        sh = v[:2]
    x = Symbol('x')
    t = Symbol('t')
    ch = ""
    d = []
    if vrex(v) == 0:
        m = simplify(diff(sympify(v), x))
        n = simplify(integrate(sympify(u), x))
    else:
        m = simplify(diff(sympify(v), t))
        n = simplify(integrate(sympify(u), t))
    print("v=", v, "--> v1=", m)
    print("u1=", u, "--> u=", n)
    print("requires", p, "integration by parts")
    i = 0
    while i < p:
        j = simplify(sympify('(' + str(n) + ')*(' + v + ')'))
        k = simplify(sympify('(' + str(n) + ')*(' + str(m) + ')'))
        if len(ch) != 0:
            ch = str(expand(simplify(sympify(ch + '-' + str(j))))) + '-||' + str(k)
        else:
            ch = str(simplify(sympify(ch + str(j)))) + '-||' + str(k)
        print(ch)
        if i < p - 1:
            d = divs(str(k), sh)
            v = d[0]
            u = d[1]
            if vrex(v) == 0:
                m = simplify(diff(sympify(v), x))
                n = simplify(integrate(sympify(u), x))
            else:
                m = simplify(diff(sympify(v), t))
                n = simplify(integrate(sympify(u), t))
            print("v=", v, "--> v1=", m)
            print("u1=", u, "--> u=", n)
            ch = ch[:ch.index('|') - 1]
        i = i + 1
    return ch

def divs(u, ch):
    d = []
    u = str(sympify(u))
    if '/' not in u and u.count(ch) == 1:
        d = simp(u)
        if len(d) == 3:
            if ch == 'ex':
                if '**' in u[:d[1] + 1] and (u[:d[1]].count('x') == 1 or u[:d[1]].count('t') == 1):
                    return [u[:d[1]], u[d[1] + 1:], int(u[d[1] - 1])]
                elif u[:d[1]].count('x') == 1 or u[:d[1]].count('t') == 1:
                    return [u[:d[1]], u[d[1] + 1:], 1]
                else:
                    return -1
            else:
                if suit(u, d[1] + 5) + 1 != len(u) and u[suit(u, d[1] + 5) + 1:suit(u, d[1] + 5) + 3] == '**':
                    return [u[d[1] + 1:suit(u, d[1] + 5) + 4], u[:d[1]], int(u[len(u) - 1])]
                else:
                    return [u[d[1] + 1:], u[:d[1]], 1]
        elif len(d) == 2:
            if u[len(u) - 3:len(u) - 1] == '**':
                return [u, '1', int(u[len(u) - 1])]
            else:
                return [u, '1', 1]
        else:
            return -1
    elif '/' in u and (ch == 'at' or ch == 'as' or ch == 'ac' or ch == 'lo') and ch in u[:u.index('/')]:
        i = 0
        sh = ""
        ah = ""
        while i < len(u):
            if u[i:i + 2] == ch:
                sh = sh + u[i:suit(u, i + 4) + 1]
                if u[suit(u, i + 4) + 1:suit(u, i + 4) + 3] == '**':
                    sh = sh + u[suit(u, i + 4) + 1:suit(u, i + 4) + 4]
                    i = suit(u, i + 4) + 4
                else:
                    i = suit(u, i + 4) + 1
            else:
                ah = ah + u[i]
                i = i + 1
        ah = ah[:ah.index('/')] + '1' + ah[ah.index('/'):]
        if sh[len(sh) - 3:len(sh) - 1] == '**':
            return [sh, str(sympify(ah)), int(sh[len(sh) - 1])]
        else:
            return [sh, str(sympify(ah)), 1]
    else:
        return -1

def polyn(u):
    k = 0
    for i in range(0, len(u)):
        if u[i] == ' ' or u[i] == '*' or u[i] == 'x' or u[i] == 't' or u[i] == '-' or u[i] == '+' or u[i].isdigit() or u[i] == '(' or u[i] == ')' or u[i] == I or (u[i] == '/' and u[i + 1].isdigit()):
            k = k + 1
    if k == len(u):
        return 0
    else:
        return 1

def chgvariable(ch, u):
    x = Symbol('x')
    t = Symbol('t')
    a = poly(sympify(u[u.index('('):]))
    c = a.all_coeffs()
    if u[0:2] == 'sq':
        b = str(sympify(t ** 2) / c[0])
        print("by change of variable : t=", u, ";dx=", b, "dt")
        sh = str(sympify(sympify('(t**2-' + str(c[1]) + ')/' + str(c[0]))))
    elif u[0:2] == 'ex':
        b = str(simplify('1/(' + str(c[0]) + '*t)'))
        print("by change of variable : t=", u, ";dx=", b, "dt")
    elif u[0:2] == 'lo':
        b = str(sympify('exp(t)/' + str(c[0])))
        print("by change of variable : t=", u, ";dx=", b, "dt")
    elif u[0:2] == 'at':
        b = str(sympify('(tan(t)**2+1)/' + str(c[0])))
        print("by change of variable : t=", u, ";dx=", b, "dt")
    elif u[0:2] == 'as':
        b = str(sympify('cos(t)/' + str(c[0])))
        print("by change of variable : t=", u, ";dx=", b, "dt")
    elif u[0:2] == 'ac':
        b = str(sympify('-sin(t)/' + str(c[0])))
        print("by change of variable : t=", u, ";dx=", b, "dt")
    elif u[0] == '(' and u[suit(u, 0) + 1:suit(u, 0) + 3] == '**':
        b = str(sympify('(t**(' + u[suit(u, 0) + 3:len(u)] + '))/' + str(c[0])))
        print("by change of variable : t=", u, ";dx=", b, "dt")
        sh = str(sympify('(t**(' + u[suit(u, 0) + 3:len(u)] + ')-' + str(c[1]) + ')/' + str(c[0])))
    ah = ""
    i = 0
    while i < len(ch):
        if ch[i:i + len(u)] == u:
            ah = ah + 't'
            i = i + len(u)
        elif ch[i] == 'x' and ch[i - 1] != 'e':
            ah = ah + sh
            i = i + 1
        else:
            ah = ah + ch[i]
            i = i + 1
    ah = str(simplify(sympify('(' + ah + ')*(' + b + ')')))
    print(ah)
    return (ah)

def xnexp(u):
    d = []
    x = Symbol('x')
    t = Symbol('t')
    d = divs(u, 'ex')
    ch = parparti(d[0], d[1], d[2])
    if vrex(u) == 0:
        s = integrate(sympify(u), x)
    else:
        s = integrate(sympify(u), t)
    print("=", s)
    return s

def xnexpcos(u):
    sh = ""
    d = []
    x = Symbol('x')
    a = poly(sympify(u[u.index('s') + 2:suit(u, u.index('s') + 1)]))
    b = poly(sympify(u[u.index('p') + 2:suit(u, u.index('p') + 1)]))
    c = a.all_coeffs()
    d = b.all_coeffs()
    if u[suit(u, u.index('s') + 1) + 1:suit(u, u.index('s') + 1) + 3] == '**':
        c[0] = c[0] * int(u[suit(u, u.index('s') + 1) + 3])
    f = sympify('exp((' + str(d[0]) + '+' + str(I * c[0]) + ')*x +' + str(c[1]) + '+' + str(d[1]) + ')')
    d = simp(u)
    sh = u[:d[1] + 1] + str(f)
    print("=", sh)
    sh = xnexp(sh)
    sh = str(sh)
    print("=real(", sh, ")")
    h = integrate(sympify(u), x)
    print("=", h)

def xnexpsin(u):
    sh = ""
    d = []
    x = Symbol('x')
    a = poly(sympify(u[u.index('n') + 2:suit(u, u.index('n') + 1)]))
    b = poly(sympify(u[u.index('p') + 2:suit(u, u.index('p') + 1)]))
    c = a.all_coeffs()
    d = b.all_coeffs()
    if u[suit(u, u.index('n') + 1) + 1:suit(u, u.index('n') + 1) + 3] == '**':
        c[0] = c[0] * int(u[suit(u, u.index('n') + 1) + 3])
    f = sympify('exp((' + str(d[0]) + '+' + str(I * c[0]) + ')*x +' + str(c[1]) + '+' + str(d[1]) + ')')
    d = simp(u)
    sh = u[:d[1] + 1] + f
    print(sh)
    sh = xnexp(sh)
    print("img(", sh, ")")
    h = integrate(sympify(u), x)
    print("=", h)

def xncos(u):
    sh = ""
    x = Symbol('x')
    t = Symbol('t')
    a = poly(sympify(u[u.index('s') + 2:suit(u, u.index('s') + 1)]))
    c = a.all_coeffs()
    if u[suit(u, u.index('s') + 1) + 1:suit(u, u.index('s') + 1) + 3] == '**':
        c[0] = c[0] * int(u[suit(u, u.index('s') + 1) + 3])
    if vrex(u) == 0:
        f = sympify('exp((' + str(I * c[0]) + ')*x +' + str(c[1]) + ')')
    else:
        f = sympify('exp((' + str(I * c[0]) + ')*t +' + str(c[1]) + ')')
    d = simp(u)
    sh = u[:d[1] + 1] + str(f)
    print(sh)
    sh = xnexp(sh)
    sh = str(sh)
    print("real(", sh, ")")
    if vrex(u) == 0:
        h = integrate(sympify(u), x)
    else:
        h = integrate(sympify(u), t)
    print("=", h)

def xnsin(u):
    sh = ""
    x = Symbol('x')
    t = Symbol('t')
    a = poly(sympify(u[u.index('n') + 2:suit(u, u.index('n') + 1)]))
    c = a.all_coeffs()
    if u[suit(u, u.index('n') + 1) + 1:suit(u, u.index('n') + 1) + 3] == '**':
        c[0] = c[0] * int(u[suit(u, u.index('n') + 1) + 3])
    if vrex(u) == 0:
        f = sympify('exp((' + str(I * c[0]) + ')*x +' + str(c[1]) + ')')
    else:
        f = sympify('exp((' + str(I * c[0]) + ')*t +' + str(c[1]) + ')')
    d = simp(u)
    sh = u[:d[1] + 1] + str(f)
    print(sh)
    sh = xnexp(sh)
    sh = str(sh)
    print("im(", sh, ")")
    if vrex(u) == 0:
        h = integrate(sympify(u), x)
    else:
        h = integrate(sympify(u), t)
    print("=", h)

def seq(u, n):
    if n == 0 or n == 1:
        i = ind(u, 'i', 0)
        k = 0
        while k == 0 and i != -1:
            if i + 6 >= len(u) or (u[i + 5:i + 7] == '**' and ((u[i + 7] != '(' and int(u[i + 7]) % 2 == 1) or (u[i + 7] == '(' and int(u[i + 9]) % 2 == 1))) or u[i + 5:i + 7] != '**':
                k = 1
            i = ind(u, 'i', i + 1)
    if n == 0 or n == 2:
        j = ind(u, 'o', 0)
        m = 0
        while m == 0 and j != -1:
            if j + 6 >= len(u) or (u[j + 5:j + 7] == '**' and ((u[j + 7] != '(' and int(u[j + 7]) % 2 == 1) or (u[j + 7] == '(' and int(u[j + 9]) % 2 == 1))) or u[j + 5:j + 7] != '**':
                m = 1
            j = ind(u, 'o', j + 1)
    if n == 0:
        if m == 0 and k == 0:
            return 0
        else:
            return 1
    elif n == 1:
        if k == 0:
            return 0
        else:
            return 1
    else:
        if m == 0:
            return 0
        else:
            return 1

def bioche(u):
    x = Symbol('x')
    t = Symbol('t')
    k = 0
    u = str(expand_trig(sympify(u)))
    print(u)
    if seq(str(expand_trig(simplify(sympify('(' + u + ')*(-1/sin(x))')))), 1) == 0:
        k = 1
        sh = str(expand_trig(simplify(sympify('(' + u + ')*(-1/sin(x))'))))
    elif seq(str(expand_trig(simplify(sympify('(' + u + ')*(1/cos(x))')))), 2) == 0:
        k = 2
        sh = str(expand_trig(simplify(sympify('(' + u + ')*(1/cos(x))'))))
    elif seq(u, 0) == 0:
        k = 3
    if k == 1:
        print("by change of variable : t=", cos(x), ";dx=", -1 / sin(x), "dt")
        print(sh)
        i = 0
        ch = ""
        while i < len(sh):
            if sh[i:i + 2] == 'co':
                ch = ch + 't'
                i = i + 6
            elif sh[i:i + 2] == 'si':
                ch = ch + '(sqrt(1-t**2))'
                i = i + 6
            elif sh[i:i + 2] == 'ta':
                ch = ch + '((sqrt(1-t**2))/t)'
                i = i + 6
            else:
                ch = ch + sh[i]
                i = i + 1
    elif k == 2:
        print("by change of variable : t=", sin(x), ";dx=", 1 / cos(x), "dt")
        print(sh)
        i = 0
        ch = ""
        while i < len(sh):
            if sh[i:i + 2] == 'si':
                ch = ch + 't'
                i = i + 6
            elif sh[i:i + 2] == 'co':
                ch = ch + '(sqrt(1-t**2))'
                i = i + 6
            elif sh[i:i + 2] == 'ta':
                ch = ch + '(t/(sqrt(1-t**2)))'
                i = i + 6
            else:
                ch = ch + sh[i]
                i = i + 1
    elif k == 3:
        print("by change of variable : t=", tan(x), ";dx=", 1 / (1 + t ** 2), "dt")
        sh = str(expand_trig(simplify(sympify('(' + u + ')*(1/(1+t**2))'))))
        print(sh)
        i = 0
        ch = ""
        while i < len(sh):
            if sh[i:i + 2] == 'si':
                ch = ch + '(sqrt(1/(1+t**2)))'
                i = i + 6
            elif sh[i:i + 2] == 'co':
                ch = ch + '(sqrt(t**2/(1+t**2)))'
                i = i + 6
            else:
                ch = ch + sh[i]
                i = i + 1
    else:
        print("by change of variable : t=", tan(x / 2), ";dx=", 2 / (1 + t ** 2), "dt")
        sh = str(expand_trig(simplify(sympify('(' + u + ')*(2/(1+t**2))'))))
        print(sh)
        i = 0
        ch = ""
        while i < len(sh):
            if sh[i:i + 2] == 'si':
                ch = ch + '(2*t/(1+t**2))'
                i = i + 6
            elif sh[i:i + 2] == 'co':
                ch = ch + '((1-t**2)/(1+t**2))'
                i = i + 6
            else:
                ch = ch + sh[i]
                i = i + 1
    ch = str(simplify(sympify(ch)))
    print("=", ch)
    return ch

def sincos(u):
    x = Symbol('x')
    t = Symbol('t')
    j = ind(u, ')', 0)
    k = ind(u, ')', j + 1)
    i = u.index('n')
    n = u.index('o')
    if ind(u, ')', i) + 1 == len(u) or u[ind(u, ')', i) + 1:ind(u, ')', i) + 3] != '**':
        m = 1
    else:
        m = int(u[ind(u, ')', i) + 3])
    if ind(u, ')', n) + 1 == len(u) or u[ind(u, ')', n) + 1:ind(u, ')', n) + 3] != '**':
        p = 1
    else:
        p = int(u[ind(u, ')', n) + 3])
    m1 = (m - 1) / 2
    p1 = (p - 1) / 2
    if m % 2 == 1 and p % 2 == 1:
        m1 = int(m1)
        p1 = int(p1)
        print("by change of variable : t=", cos(2 * x), ";dx=", -1 / sin(2 * x), "dt")
        ch = '(1/2**(' + str(m1) + '+' + str(p1) + '+' + str(2) + '))*(1-t)**' + str(m1) + '*(1+t)**' + str(p1)
        ch = sympify(ch)
    elif m % 2 == 1 and p % 2 == 0:
        m1 = int(m1)
        print("by change of variable : t=", cos(x), ";dx=", -1 / sin(x), "dt")
        ch = (1 - t ** 2) ** m1 * t ** p
    elif m % 2 == 0 and p % 2 == 1:
        p1 = int(p1)
        print("by change of variable : t=", sin(x), ";dx=", 1 / cos(x), "dt")
        ch = (1 - t ** 2) ** p1 * t ** m
    else:
        print("by formul euler")
        ch = ((exp(I * x) - exp(-I * x)) / (2 * I)) ** m * ((exp(I * x) + exp(-I * x)) / 2) ** p
    print(ch)
    ch = simplify(expand(ch))
    print(ch)
    ch = integrate(sympify(u), x)
    print(ch)
    return str(ch)

def coss(u):
    x = Symbol('x')
    t = Symbol('t')
    q = u.rfind('**')
    n = int(u[q + 2])
    if n == 2:
        if 'x' in u:
            ch = '(1+cos(2*x))/2'
        else:
            ch = '(1+cos(2*t))/2'
        print(u, "=", ch)
    elif n % 2 == 0 and n != 2:
        if 'x' in u:
            ch = '((exp(I*x)+exp(-I*x))/2)**' + str(n)
        else:
            ch = '((exp(I*t)+exp(-I*t))/2)**' + str(n)
        print(u, "=", ch)
        ch = expand(ch)
        print("=", ch)
        ch = simplify(ch)
        print("=", ch)
    else:
        if 'x' in u:
            ch = 'cos(x)*(cos(x)**2)**((' + str(n) + '-1)/2)'
        else:
            ch = 'cos(t)*(cos(t)**2)**((' + str(n) + '-1)/2)'
        print(u, "=", sympify(ch))
        if 'x' in u:
            ch = 'cos(x)*(1-sin(x)**2)**((' + str(n) + '-1)/2)'
        else:
            ch = 'cos(t)*(1-sin(t)**2)**((' + str(n) + '-1)/2)'
        print("=", sympify(ch))
        ch = expand(sympify(ch))
        print("=", ch)
    if 'x' in u:
        ch = integrate(sympify(ch), x)
    else:
        ch = integrate(sympify(ch), t)
    print(ch)
    return ch

def sins(u):
    x = Symbol('x')
    t = Symbol('t')
    q = u.rfind('**')
    n = int(u[q + 2])
    if n == 2:
        if 'x' in u:
            ch = '(1-cos(2*x))/2'
        else:
            ch = '(1-cos(2*t))/2'
        print(u, "=", ch)
    elif n % 2 == 0 and n != 2:
        if 'x' in u:
            ch = '((exp(I*x)-exp(-I*x))/(2*I))**' + str(n)
        else:
            ch = '((exp(I*t)-exp(-I*t))/(2*I))**' + str(n)
        print(u, "=", ch)
        ch = expand(ch)
        print("=", ch)
        ch = simplify(ch)
        print("=", ch)
    else:
        if 'x' in u:
            ch = 'sin(x)*(sin(x)**2)**((' + str(n) + '-1)/2)'
        else:
            ch = 'sin(t)*(sin(t)**2)**((' + str(n) + '-1)/2)'
        print(u, "=", sympify(ch))
        if 'x' in u:
            ch = 'sin(x)*(1-cos(x)**2)**((' + str(n) + '-1)/2)'
        else:
            ch = 'sin(t)*(1-cos(t)**2)**((' + str(n) + '-1)/2)'
        print("=", sympify(ch))
        ch = expand(sympify(ch))
        print("=", ch)
    if 'x' in u:
        ch = integrate(sympify(str(ch)), x)
    else:
        ch = integrate(sympify(str(ch)), t)
    print("=", ch)
    return ch

def expver(u, c):
    d = ['exp(', 'sin(', 'cos(', 'sqrt(', 'atan(', 'acos(', 'asin(', 'log(']
    l = simp(u)
    n = 1
    m = 1
    if len(l) == len(c) + 1:
        n = 0
    if c[0] == -1:
        if polyn(u[l[0] + 1:l[1]]) == 0:
            del (l[0])
            del (c[0])
    if c[0] != -1:
        m = 0
    i = 0
    k = 0
    while i < len(d) and k == 0:
        if d[i] in u and (vrex(u[ind(u, '(', u.find(d[i])):suit(u, ind(u, '(', u.find(d[i])))]) == 0 or vret(u[ind(u, '(', u.find(d[i])):suit(u, ind(u, '(', u.find(d[i])))]) == 0) and d[i] not in c:
            k = 1
        i = i + 1
    j = 0
    f = 0
    while j < len(c) and n == 0 and k == 0:
        if c[j] not in u:
            f = 1
        j = j + 1
    if n == 0 and m == 0 and k == 0 and f == 0:
        return 0
    else:
        return 1

def ver1(u, n, m):
    d = ['exp(', 'sin(', 'cos(', 'sqrt(', 'atan(', 'acos(', 'asin(', 'log(']
    k = 0
    i = 0
    while i < len(d) and k == 0:
        if d[i] in u and d[i] != n:
            k = 1
        i = i + 1
    if m == 1:
        s = 0
        j = 0
        while j < len(u) and s == 0:
            if u[j] == 'x' and u[j - 1] != 'e' and u[:j].count(')') == u[:j].count('('):
                s = 1
            j = j + 1
    if m == 2:
        p = 0
        f = 0
        while p < len(u) and f == 0:
            if u[p] == 't' and degree(sympify(u[p + 2:suit(u, p + 2)])) != 1:
                f = 1
            p = p + 1
    if m == 1:
        if k == 0 and s == 0:
            return 0
        else:
            return 1
    if m == 2:
        if k == 0 and f == 0:
            return 0
        else:
            return 1
    if m == 0:
        if k == 0:
            return 0
        else:
            return 1

def ver2(u):
    c = []
    m = -1
    if (u.count('sqrt') == 2 and deri(u) == 1) or (u.count('sqrt') == 1 and deri(u) == 0) and ver1(u, 'sqrt(', 0) == 0 and degree(sympify(u[u.index('t') + 2:suit(u, u.index('t') + 2)])) == 2:
        c = poly(sympify(u[u.index('t') + 2:suit(u, u.index('t') + 2)])).all_coeffs()
        if c[2] != 1 or c[1] != 0:
            m = 0
    if ver1(u, 'sqrt(', 0) == 0:
        i = ind(u, 't', 0)
        k = 0
        while i != -1 and k == 0:
            if poly(sympify(u[u.index('t') + 2:suit(u, u.index('t') + 2)])).all_coeffs() != [-1, 0, 1]:
                k = 1
            i = ind(u, 't', i + 1)
        if k == 0:
            m = 1
    return m

def simexp(u):
    l = 10
    d = []
    ch = ""
    for i in range(0, len(u)):
        if u[i] == 'p':
            d = poly(sympify(u[i + 2:suit(u, i + 2)])).all_coeffs()
            if d[0] < l:
                l = d[0]
    j = 0
    while j < len(u):
        if u[j:j + 3] == 'exp':
            d = poly(sympify(u[j + 4:suit(u, j + 4)])).all_coeffs()
            ch = ch + str(sympify('exp(' + str(l) + '*x)')) + '**(' + str(d[0]) + '/' + str(l) + ')'
            j = suit(u, j + 4) + 1
        else:
            ch = ch + u[j]
            j = j + 1
    print((ch))
    ch = chgvariable(ch, str(sympify('exp(' + str(l) + '*x)')))
    return ch

def ren(u):
    k = 0
    i = 0
    while i < len(u) and k == 0:
        if u[i].isalpha() and u[i] != 'x' and u[i] != 't':
            j = ind(u, '(', i)
            while j < suit(u, j) and k == 0:
                if u[j].isalpha() and u[j] != 'x' and u[j] != 't':
                    k = 1
                j = j + 1
        i = i + 1
    if k == 1:
        ch = chgvariable(u, u[j - 1:suit(u, ind(u, '(', j)) + 1])
        return ch
    return u

def ren1(u):
    k = 0
    i = 0
    while i < len(u) and k == 0:
        if u[i].isalpha() and u[i] != 'x' and u[i] != 't':
            j = ind(u, '(', i)
            a = suit(u, j)
            while j < a and k == 0:
                if u[j].isalpha() and u[j] != 'x' and u[j] != 't':
                    k = 1
                j = j + 1
        i = i + 1
    if k == 1:
        return 0
    else:
        return 1

def racine3(u):
    ah = ""
    c = []
    j = u.index('t')
    a = poly(sympify(u[j + 2:suit(u, j + 2)]))
    c = a.all_coeffs()
    a1 = str(sympify('sqrt(-' + str(c[0]) + ')'))
    b = str(sympify(str(c[1]) + '/(2*' + a1 + ')'))
    c = str(sympify(str(c[2]) + '+' + b + '**2'))
    ch = sympify('sqrt(' + c + '-(' + a1 + '*x-' + b + ')**2)')
    print(u, "=", ch)
    if len(u[:u.index('s')]) != 0 and u[:u.index('s')] != ' ':
        c = str(sympify(u[:u.index('s')] + '*' + c))
    print(sympify('sqrt(' + '(' + c + ')' + ')*sqrt(1-((' + a1 + '*x-' + b + ')/sqrt(' + c + '))**2)'))
    print("sin(t)=", sympify('(' + a1 + '*x-' + b + ')/sqrt(' + c + ')'))
    sh = str(sympify(c + '*sqrt(1-sin(t))'))
    print(sh)
    sh = str(sympify('(' + c + ')' + '*cos(t)**2'))
    print(sh)
    return sh

def racine4(u):
    ch = ""
    print("put:x=sin(t)")
    i = 0
    while i < len(u):
        if u[i] == 'x':
            ch = ch + 'sin(t)'
        else:
            ch = ch + u[i]
        i = i + 1
    ch = str(simplify(sympify('(' + ch + ')*(cos(t))')))
    print("=", ch)
    return ch

def racine5(u):
    c = []
    d = []
    ch = ""
    t = Symbol('t')
    a = poly(sympify(u[u.index('t') + 2:ind(u, '/', u.index('t'))]))
    b = poly(sympify(u[ind(u, '/', u.index('t')) + 1:ind(u, ')', ind(u, '/', u.index('t'))) + 1]))
    c = a.all_coeffs()
    d = b.all_coeffs()
    if len(c) == 2 and len(d) == 2 and d[0] == c[0]:
        print("put:t=", u[u.index('s'):suit(u, u.index('s') + 4) + 1])
        j = (c[1] - t ** 2 * d[1]) / (c[0] * (t ** 2 - 1))
        print("dx=", simplify(diff(j, t)))
        i = 0
        while i < len(u):
            if u[i] == 'x':
                ch = ch + str(j)
                i = i + 1
            elif u[i] == 's':
                ch = ch + 't'
                i = suit(u, u.index('s') + 4) + 1
            else:
                ch = ch + u[i]
                i = i + 1
        ch = str(simplify(sympify(ch + '*(' + str(diff(j, t)) + ')')))
        print("=", ch)
        return ch

def prim(u, fh):
    d = []
    s = str(sympify(u))
    if '/' in u and polyn(u[:u.index('/')]) == 0 and polyn(u[u.index('/') + 1:]) == 0:
        u = polys(u)
        primitive(u, fh)
    if '/' in u and 'exp(' in u[u.index('/'):] and ver1(u, 'exp(', 1) == 0:
        u = simexp(u)
        primitive(u, fh)
    elif u.count('sqrt(') == 1 and '/' in u[u.index('s'):suit(u, u.index('s') + 4)] and degree(sympify(u[u.index('t') + 2:ind(u, '/', u.index('t'))])) == 1:
        u = racine5(u)
        primitive(u, fh)
    elif '/' in u and 'sqrt(' in u and ver1(u, 'sqrt(', 2) == 0:
        u = chgvariable(u, u[u.index('s'):suit(u, u.index('t') + 2) + 1])
        primitive(u, fh)
    elif '/' in u and 'sqrt(' in u[u.index('/'):] and ver2(u) == 0:
        u = racine1(u)
        if deri(u) > 0:
            d = derivp(u)
            j = u[:d[1]]
            print(Integral(sympify(j), pp(j)), "=", integrate(sympify(j), pp(j)))
            j = str(integrate(sympify(j)))
            u = u[d[1] + 1:]
            u = racine0(u)
            u = j + '+' + str(u)
            print("=", sympify(u))
        else:
            u = racine0(u)
    elif divsio(u) != -1 and 'sqrt(' in u and ver2(u) == 1:
        u = racine4(u)
        if 'sqrt(' in u:
            u = u[:u.index('q') - 1] + 'cos(t)' + u[suit(u, u.index('r') + 2) + 1:]
            u = str(expand(simplify(sympify(u))))
            print("==", u)
        primitive(u, fh)
    elif 'sqrt(' in u and (ver2(u) == 0 or ver2(u) == 1):
        u = racine2(u)
        if deri(u) > 0:
            d = derivp(u)
            j = u[:d[1] + 1]
            u = u[d[1] + 1:]
            u = racine3(u)
            u = j + u
            u = str(sympify(u))
        else:
            u = racine3(u)
        primitive(u, fh)
    elif '/' in u and ('sin(' in u[u.index('/'):] or 'cos(' in u[u.index('/'):]):
        u = bioche(u)
        primitive(u, fh)
    elif ren1(u) == 0:
        u = ren(u)
        primitive(u, fh)
    elif divs(u, 'lo') != -1:
        d = divs(u, 'lo')
        u = parparti(d[0], d[1], d[2])
        primitive(u, fh)
    elif divs(u, 'at') != -1:
        d = divs(u, 'at')
        u = parparti(d[0], d[1], d[2])
        primitive(u, fh)
    elif divs(u, 'ac') != -1:
        d = divs(u, 'ac')
        u = parparti(d[0], d[1], d[2])
        primitive(u, fh)
    elif divs(u, 'as') != -1:
        d = divs(u, 'as')
        u = parparti(d[0], d[1], d[2])
        primitive(u, fh)
    else:
        y = 1

def on_enter(g):
    i = 0
    while i < len(g) - 1:
        if ((g[i] == 'x' and (i + 1 == len(g) or g[i + 1] != 'p')) or g[i].isdigit() or g[i] == ')'):
            if g[i + 1] not in ['+', '-', '^', '*', ')', '/']:
                g = g[:i + 1] + '*' + g[i + 1:]
                i += 1
        i += 1
    g = g.replace('√', 'sqrt').replace('^', '**')
    return sympify(g)

def primitivs(u, n1, m1):
    u = u.replace('√', 'sqrt').replace('^', '**')
    x = Symbol('x')
    if n1 == 0 and m1 == 0:
        fh = integrate(sympify(u), x)
    else:
        fh = integrate(sympify(u), (x, n1, m1))
    primitive(u, fh)

@app.post("/run")
def run_main(params: dict = None):
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    try:
        if params and "func" in params:
            primitivs(params["func"], 0, 0)
        else:
            print("Aucun paramètre fourni")
    except Exception as e:
        sys.stdout = old_stdout
        return JSONResponse({"error": str(e)}, status_code=500)

    sys.stdout = old_stdout
    logs = buffer.getvalue().splitlines()

    return JSONResponse({
        "logs": logs,
        "status": "completed"
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("prim:app", host="0.0.0.0", port=8000, reload=True)

    
