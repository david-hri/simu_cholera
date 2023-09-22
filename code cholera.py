import random
import matplotlib.pyplot as plt
import numpy as np


class Personne:
    def __init__(self, x, y):
            self.x = x
            self.y = y
            if random.random()<=vacc*eff:
                self.state="Recovered"
            else:
                self.state="Sane"
            self.maisonx=x
            self.maisony=y


class Puit:
    def __init__(self, x, y):
            self.x = x
            self.y = y
            self.state="Sane"

puit={}
personne={}
show=True
xmax=10
ymax=10
n=500
N=100
N_hopitaux=int(n/100*2)
npuit=5
pi=0.3
r=20  #arbitraire
pr=0.15
pe=0.3   #arbitraire
pp=0.1
pd_hp=2/100
pd_no_hp=25/100
vacc=0.5 #arbitraire
eff=0.9


def init(n,npuit,xmax,ymax):
    for i in range(n):
        personne[str(i)]=Personne(random.random()*xmax,random.random()*ymax)
    for i in range(npuit):
        puit[str(i)]=Puit(random.random()*xmax,random.random()*ymax)


init(n,npuit,10,10)
puit["0"].state="Infected"
fig, ax =plt.subplots()



personne_saine =ax.scatter([personne[str(i)].x for i in range(n)],[personne[str(i)].y for i in range(n)],s=20,c='r')

personne_inf=ax.scatter([],[],s=20,c='g')

Puit_sain =ax.scatter([puit[str(i)].x for i in range(1,npuit)],[puit[str(i)].y for i in range(1,npuit)],s=300,c='b')

Puit_inf =ax.scatter([puit[str(i)].x for i in range(1)],[puit[str(i)].y for i in range(1)],s=300,c='darkgreen')


def dist(personne,i,puit):
    min=100000
    imin=0
    for j in range(npuit):
        x=((puit[str(j)].x-personne[str(i)].x)**2+(puit[str(j)].y-personne[str(i)].y)**2)**1/2
        if x<min:
            min=x
            imin=j
    return imin

def main():
    S,E,I,R=[],[],[],[]
    Ip,Is=[],[]
    for i in range(n):
        if personne[str(i)].state=="Sane":
            j=dist(personne,i,puit)
            if puit[str(j)].state=="Infected":
                if random.random()<=pi:
                    personne[str(i)].state="Exposed"
        if personne[str(i)].state=="Exposed":
            if random.random()<=pe:
                personne[str(i)].state="Infected"
        if personne[str(i)].state=="Infected":
            if random.random()<=pr:
                personne[str(i)].state="Recovered"
        elif personne[str(i)].state=="Exposed":
            j=dist(personne,i,puit)
            if random.random()<=pp:
                puit[str(j)].state="Infected"



        if personne[str(i)].state=="Sane":
            S.append(i)
        elif personne[str(i)].state=="Infected":
            I.append(i)
        elif personne[str(i)].state=="Exposed":
            E.append(i)
        else:
            R.append(i)
    for i in range(npuit):
        if puit[str(i)].state=="Infected":
            Ip.append(i)
        else:
            Is.append(i)
    return S,E,I,R,Is,Ip




def Puit_state():
    Ps,Pi=[],[]
    for i in range(npuit):
        if puit[str(i)].state=="Sane":
            Ps.append(i)
        else:
            Pi.append(i)
    return Ps,Pi



def move(S,E):
    for i in E:
        ok=True
        while ok:
            l=random.random()*xmax/10
            theta=random.random()*2*np.pi
            if personne[str(i)].x+l*np.cos(theta)<=xmax and personne[str(i)].x+l*np.cos(theta)>=0 and personne[str(i)].y+l*np.sin(theta)<=ymax and personne[str(i)].y+l*np.sin(theta)>=0 and abs(personne[str(i)].x+l*np.cos(theta)-personne[str(i)].maisonx)<=xmax/r and abs(personne[str(i)].y+l*np.sin(theta)-personne[str(i)].maisony)<=ymax/r:
                ok=False
                personne[str(i)].x=personne[str(i)].x+l*np.cos(theta)
                personne[str(i)].y=personne[str(i)].y+l*np.sin(theta)

    for i in S:
        ok=True
        while ok:
            l=random.random()*xmax/10
            theta=random.random()*2*np.pi
            if personne[str(i)].x+l*np.cos(theta)<=xmax and personne[str(i)].x+l*np.cos(theta)>=0 and personne[str(i)].y+l*np.sin(theta)<=ymax and personne[str(i)].y+l*np.sin(theta)>=0 and abs(personne[str(i)].x+l*np.cos(theta)-personne[str(i)].maisonx)<=xmax/r and abs(personne[str(i)].y+l*np.sin(theta)-personne[str(i)].maisony)<=ymax/r:
                ok=False
                personne[str(i)].x=personne[str(i)].x+l*np.cos(theta)
                personne[str(i)].y=personne[str(i)].y+l*np.sin(theta)




Sg,Ig,Rg,Eg,Hp=[n*(1-vacc*eff)],[0],[n*vacc*eff],[0],[0]
def graphe(show=True):
    for i in range(N):
        ax.scatter([0],[0],s=3000000,c='w')
        S,E,I,R,Is,Ip=main()
        Ps,Pi=Puit_state()
        Sg.append(len(S))
        Ig.append(len(I))
        Rg.append(len(R))
        Eg.append(len(E))
        x=len(I)-N_hopitaux
        Hp.append(max(x,0))
        if show:

            personne_saine =ax.scatter([personne[str(i)].x for i in S],[personne[str(i)].y for i in S],s=20,c='r')
            personne_inf=ax.scatter([personne[str(i)].x for i in I],[personne[str(i)].y for i in I],s=20,c='g',)
            personne_r=ax.scatter([personne[str(i)].x for i in R],[personne[str(i)].y for i in R],s=20,c='grey')
            personne_e=ax.scatter([personne[str(i)].x for i in E],[personne[str(i)].y for i in E],s=20,c='purple')
            Puit_sain =ax.scatter([puit[str(i)].x for i in Is ],[puit[str(i)].y for i in Is],s=300,c='b')

            Puit_inf =ax.scatter([puit[str(i)].x for i in Ip],[puit[str(i)].y for i in Ip],s=300,c='darkgreen')

            plt.pause(0.2/(i+1)) # pause avec duree en secondes

        move(S,E)
    return Ip


Ip=graphe(show)

print("Le nombre total de puits infectés est", str(len(Ip)))
prop=sum(Hp)/sum(Ig)
décès=(pd_hp*(1-prop)*Rg[-1]+pd_no_hp*prop*Rg[-1])*(1-eff*vacc)
évitable=décès-pd_hp*Rg[-1]*(1-eff*vacc)

print("A la fin de l'épidémie on obtient environ",str(int(décès)),"dont environ",str(int(évitable)),"morts évitables")
Rg[0]=Rg[1]
Sg[0]=Sg[1]

fig.clear()

plt.plot([i for i in range(len(Sg))],Sg,label="Sain")
plt.plot([i for i in range(len(Eg))],Eg,label='Exposé')
plt.plot([i for i in range(len(Ig))],Ig,label="Infecté")
plt.plot([i for i in range(len(Rg))],Rg,label="Guéri")
plt.legend()
plt.show()

