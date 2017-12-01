# README
## 1.Come Iniziare
Per iniziare è necessario installare **gym**, la libreria open-source che ci permette di avere accesso ai diversi environments.
Per fare ciò aprire il terminale e digitare
```bash
git clone https://github.com/openai/gym.git
cd gym
pip install -e 
```
Tuttavia in questo modo è possibile utilizzare solamente poche categorie di environments:

1. algoritmich
2. toy-text
3. classic-control

Per utilizzare tutti gli altri environments è necessario installare delle ulteriori dipendenze.
Le istruzioni per l'installazione delle diverse dipendenze si trovano al seguente link:  https://github.com/openai/gym

## 2.Gym
Il cuore di gym è l'interfaccia **Env**, per il cui utilizzo è necessario conoscere 3 metodi fodamentali:

1. **Reset(self)**: resetta lo stato dell'environment e ritorna l'observation;
2. **Step(self, action)**: fa avanzare l'environments di un timestep. Ritorna observation, reward, done e info;
3. **Render(self, mode='human', close=False)**: renderizza un frame dell'environments. Passando come parametro il comando close si segnala al renderizzatore di chiudere ogni finestra;

# CartPole-V0
Per iniziare è necessario selezionare l'environment scelto:

```python
env = gym.make('CartPole-v0')
```
L'aspetto chiave per interfacciarsi con environments diversi è capire quali sono le **observation** ritornate ad ogni step dell'algoritmo.

## 1.Observation
In questo environment l'observation è una tupla di 4 elementi: 
 
1. **Posizione del cart**;
2. **Angolo di inclinazione del pole**;
3. **Velocità angolare del pole**;
4. **Velocità del cart**;
 
Tutte queste quattro caratteristiche vengono misurate in modo diverso e ritornate con unità di misura differenti.
E' pertanto necessario normalizzare i dati ottenuti in valori tra 0 e 99 per poter così indicizzare la matrice dei reward.

```python
cart_pos = int(interp(cart_pos,[min_env[0], max_env[0]], [0,DIM_P - 1])) 
```
Una volta normalizzati i dati è possibile individuare lo stato ottimale, ovvero quello in cui i valori della posizione del cart, dell'angolo di inclinazione del pole, della velocià angolare e della velocità del cart sono pari a 50.
self.q[cart_pos][cart_speed][angle][angle_speed][action] = pv + learning_rate * (av + alpha * max(self.q[cart_pos, cart_speed, angle, angle_speed, :]) - pv)  # aggiornamento matrice q dei reward      

## 2.Reward
Il metodo **step** ritorna un reward già implementato che da come valori 0 o 1 a seconda che lo stato sia più o meno vicino allo stato ottimale.
Per rendere più preciso e rapido l'apprendimento ho scelto di implementare il metodo **gen_matrix** che genera la matrice r dei reward.

## 3.Exploration
Il metodo **exploration** ritorna la prossima azione prendendo in input lo stato presente.
La scelta dell'azione futura può essere effettuata in modo randomico o scegliendo l'azione più redditizia.

## 4.Alg_q
All'interno del metodo **Alg_q** viene invocato il metodo **step** che ritorna **observation**, successivamente i dati vengono normalizzati e viene aggiornato il reward all'interno della matrice q.

# MsPacman-v0
Per iniziare selezionare l'environment scelto:

```python
env = gym.make('MsPacman-v0')
```

## 1.Observation
In questo environment l'observation è un immagine RGB ovvero un array di dimensioni (210,160,3).
Ogni stato dell'environment è quindi un'immagine.

## 2.Reward
Assegnare un reward ad un determinato stato è molto complicato poichè richiede un'interpretazione dell'immagine frame per frame.
Risulta pertanto più comodo utilizzare i rewards già implementati che ritorna il metodo **step**.

## 3.Exploration
Il metodo **exploration** non viene modificato e resta sostanzialmente uguale a quello degli altri environment, infatti prende in ingresso uno stato e ritorna l'azione futura dell'agente.

## 4.Alg_q
All'interno del metodo **Alg_q** viengono invocati i metodi **exploration** e **step** e viene gestita l'informazione contenuta nella variabile observation ovvero un array (210,160,3).
Viene generato un dizionario le cui chiavi sono le diverse observation e i valori associati sono i reward per le diverse azioni realizzabili.
Ogni elemento del dizionario ha quindi come chiave un array e come valori associati un insieme contenente nove reward, ognuno corrispondente ad una diversa azione.

NB: per indicizzare il dizionario con un array è prima necessario fare un hashing dell'oggetto.

```python
state = int(sha1(observation.view(uint8)).hexdigest(), 16) 
```

Una volta gestita l'observation è possibile aggiornare i reward per ogni elemento del dizionario.
  