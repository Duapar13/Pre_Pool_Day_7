<template>
    <div class="add-friend">
    <h1>Ajouter un ami</h1>
    <input v-model="newFriendName" type="text" placeholder="Nom de l'ami" />
    <button @click="addFriend">Ajouter</button>
  </div>
  <div>
    <div class="friend-requests">
      <h1>Demande d'amis</h1>
      <ul>
  <li v-for="request in friendRequests" :key="request.id">
    <div class="user-info">
      <img :src="request.photo" alt="Photo de profil de la demande d'ami" />
      {{ request.username }}
      <button @click="acceptFriendRequest(request.id)" v-if="!request.isRequester">Accepter</button>
      <button @click="deleteFriendRequest(request.id)">Supprimer</button>
    </div>
  </li>
</ul>

      </div>
    <h1>Liste des utilisateurs</h1>
    <ul>
      <li v-for="user in users" :key="user.id" @click="showMessages(user.id, 'friend')">
        <div class="user-info">
          <img :src="user.photo" alt="Photo de profil" />
          {{ user.username }} <span class="emoji">😊</span> <!-- Ajout d'un emoji -->
        </div>
      </li>
    </ul>
    
    <h1>Liste des groupes</h1>
    <ul>
      <li v-for="group in groups" :key="group.id" @click="showMessages(group.id, 'group')">
        <div class="user-info">
          <img :src="group.picture" alt="Photo du groupe" />
          {{ group.name }} <span class="emoji">👥</span> <!-- Ajout d'un emoji -->
        </div>
      </li>
    </ul>
    
    <!-- Affichage des messages des amis -->
    <div class="messages" v-if="selectedType === 'friend'">
      <h2>Messages de {{ selectedName }} <span class="emoji">💬</span></h2> <!-- Ajout d'un emoji -->
      <ul>
        <li v-for="message in messages" :key="message.id">
          <div class="message-details">
            <img :src="message.sender_photo" alt="Photo de l'expéditeur" />
            <span>{{ message.sender_username }} :</span>
            <p class="message-box"><pre>{{ message.message }}</pre></p>

            
          </div>
        </li>
      </ul>
    </div>

    <!-- Affichage des messages des groupes -->
    <div class="messages" v-else-if="selectedType === 'group'">
      <h2>Messages du groupe {{ selectedName }} <span class="emoji">📢</span></h2> <!-- Ajout d'un emoji -->
      <ul>
        <li v-for="message in messages" :key="message.id">
          <div class="message-details">
            <img :src="message.photo" alt="Photo de l'expéditeur" />
            <span>{{ message.username }} :</span>
            <p class="message-box" v-html="message.message_text"></p>

            
          </div>
        </li>
      </ul>
    </div>

    <div v-if="selectedType === 'friend' || selectedType === 'group'" class="message-input">
      <textarea v-model="newMessage" type="text" placeholder="Écrire un message..." />
      <button @click="sendMessage" :disabled="selectedId === null">Envoyer</button>
    </div>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: [], // Les utilisateurs seront stockés ici
      groups: [], // Les groupes seront stockés ici
      selectedId: null, // L'ID de l'utilisateur ou du groupe sélectionné
      selectedType: '', // Type de l'élément sélectionné ('friend' ou 'group')
      selectedName: '', // Le nom de l'utilisateur ou du groupe sélectionné
      messages: [], // Les messages seront stockés ici
      newMessage: '', // Le nouveau message à envoyer
      newFriendName: '', // Le nom de l'ami à ajouter
      friendRequests: [], // Les demandes d'amis seront stockées ici


    };
  },
  methods: {
  getNameByIdAndType(id, type) {
    // ...
  },
  acceptFriendRequest(requestId) {
      const token = localStorage.getItem('token');
      const apiUrl = `http://localhost:8100/etudik/acceptfriendrequest/${requestId}/${token}`;

      axios.post(apiUrl)
        .then(response => {
          // Gérer la réponse de l'API si nécessaire
          console.log('Demande d\'ami acceptée avec succès:', response.data);

          // Mettre à jour la liste des demandes d'amis après acceptation
          this.friendRequests = this.friendRequests.filter(request => request.id !== requestId);
        })
        .catch(error => {
          console.error('Erreur lors de l\'acceptation de la demande d\'ami :', error);
        });
    },
    deleteFriendRequest(requestId) {
      const token = localStorage.getItem('token');
      const apiUrl = `http://localhost:8100/etudik/deletefriendrequest/${requestId}/${token}`;

      axios.delete(apiUrl)
        .then(response => {
          // Gérer la réponse de l'API si nécessaire
          console.log('Demande d\'ami supprimée avec succès:', response.data);

          // Mettre à jour la liste des demandes d'amis après suppression
          this.friendRequests = this.friendRequests.filter(request => request.id !== requestId);
        })
        .catch(error => {
          console.error('Erreur lors de la suppression de la demande d\'ami :', error);
        });
    },

    

  addFriend() {
    if (!this.newFriendName) {
      // Vous pouvez ajouter une validation ici pour vous assurer que le champ n'est pas vide.
      return;
    }

    const token = localStorage.getItem('token');
    const apiUrl = `http://localhost:8100/etudik/sendrequest/${this.newFriendName}/${token}`;
    
    axios.post(apiUrl, {}, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(response => {
        // Gérer la réponse de l'API si nécessaire
        console.log('Demande d\'ajout d\'ami envoyée avec succès:', response.data);

        // Effacer le champ d'entrée après l'ajout de l'ami
        this.newFriendName = '';
      })
      .catch(error => {
        console.error('Erreur lors de l\'envoi de la demande d\'ajout d\'ami :', error);
      });
  },

  sendMessage() {
      if (!this.selectedId || !this.newMessage) {
        // Vous pouvez ajouter une validation ici pour vous assurer que l'ID de l'utilisateur ou du groupe est sélectionné
        // et que le message n'est pas vide.
        return;
      }

      const token = localStorage.getItem('token');
      let apiUrl = '';

      if (this.selectedType === 'friend') {
        apiUrl = `https://api.hbc-group.fr/etudik/sendmessagefriend/${this.selectedId}/${token}`;
      } else if (this.selectedType === 'group') {
        apiUrl = `https://api.hbc-group.fr/etudik/sendmessagegroup/${this.selectedId}/${token}`;
      }

      const requestData = {
        token: token,
        message: this.newMessage,
      };

      axios.post(apiUrl, requestData)
        .then(response => {
          // Gérer la réponse de l'API si nécessaire
          console.log('Message envoyé avec succès:', response.data);

          // Vous pouvez également mettre à jour la liste des messages ici si nécessaire
          // this.messages.push(response.data);

          // Effacer le champ de saisie après l'envoi du message
          this.newMessage = '';
        })
        .catch(error => {
          console.error('Erreur lors de l envoi du message :', error);
        });
    },
  showMessages(id, type) {
    this.selectedType = type;
  this.selectedId = id;
      const token = localStorage.getItem('token');
      if (type === 'friend') {
        const apiUrl = `https://api.hbc-group.fr/etudik/messagefriend/${token}/${id}`;
        axios.get(apiUrl)
          .then(response => {
            this.messages = response.data.messages;
            this.selectedName = this.getNameByIdAndType(id, type);
          })
          .catch(error => {
            console.error('Erreur lors de la récupération des messages :', error);
          });
      } else if (type === 'group') {
        const apiUrl = `https://api.hbc-group.fr/etudik/messagegroup/${id}`;
        axios.get(apiUrl)
          .then(response => {
            this.messages = response.data.messages;
            this.selectedName = this.getNameByIdAndType(id, type);
          })
          .catch(error => {
            console.error('Erreur lors de la récupération des messages :', error);
          });
      }
    },
    updateMessagesPeriodically() {
      setInterval(() => {
        if (this.selectedId && this.selectedType) {
          this.showMessages(this.selectedId, this.selectedType);
        }
      }, 3000); // 3000 millisecondes (3 secondes)
    },
    getNameByIdAndType(id, type) {
      // Vous devrez implémenter une méthode pour obtenir le nom réel en fonction de l'ID et du type.
      // Vous pouvez appeler une API ou utiliser vos données locales pour cela.
      // Exemple :
      if (type === 'friend') {
        const user = this.users.find(user => user.id === id);
        return user ? user.username : '';
      } else if (type === 'group') {
        const group = this.groups.find(group => group.id === id);
        return group ? group.name : '';
      }
      return '';
    },
  },
  
  mounted() {
    this.updateMessagesPeriodically();

    
  // Appel API pour récupérer la liste des utilisateurs
  const token = localStorage.getItem('token');

  axios.get(`https://api.hbc-group.fr/etudik/listfriend/${token}`)
    .then(response => {
      this.users = response.data;
    })
    .catch(error => {
      console.error('Erreur lors de la récupération des utilisateurs :', error);
    });

  // Appel API pour récupérer la liste des groupes
  axios.get(`http://localhost:8100/etudik/listrequestfriend/${token}`)
      .then(response => {
        this.friendRequests = response.data;
      })
      .catch(error => {
        console.error('Erreur lors de la récupération des demandes d\'amis :', error);
      });
  axios.get(`https://api.hbc-group.fr/etudik/listgroup/${token}`)
    .then(response => {
      this.groups = response.data;
    })
    .catch(error => {
      console.error('Erreur lors de la récupération des groupes :', error);
    });
},

}

</script>
<style scoped>
h1 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333; /* Couleur du texte */
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  cursor: pointer;
  background-color: #f5f5f5; /* Couleur de fond des éléments de la liste */
  padding: 10px;
  border-radius: 5px;
  transition: background-color 0.2s ease; /* Animation de transition de couleur de fond */
}

li:hover {
  background-color: #e0e0e0; /* Couleur de fond au survol */
}

.user-info {
  display: flex;
  align-items: center;
  color: #333; /* Couleur du texte */
}

img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

span {
  font-size: 16px;
}

.messages {
  margin-top: 20px;
}

.message-details {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f0f0f0; /* Couleur de fond des messages */
  border-radius: 5px;
}

.message-details img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}

.message-details span {
  font-size: 14px;
  font-weight: bold;
  color: #333; /* Couleur du texte du nom de l'expéditeur */
}

.message-details p {
  font-size: 16px;
  color: #555; /* Couleur du texte du message */
}
.message-details p.message-box {
  white-space: pre-wrap; /* Conserver les retours à la ligne */
  max-height: 300px; /* Hauteur maximale de la boîte de messages */
  overflow-y: auto; /* Défilement vertical automatique si nécessaire */
  padding: 10px;
  background-color: #f0f0f0; /* Couleur de fond des messages */
  border-radius: 5px;
  margin-top: 20px;
}



.message-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
  font-size: 14px;
}

.message-box {
  max-height: 300px; /* Hauteur maximale de la boîte de messages */
  overflow-y: scroll; /* Défilement vertical automatique */
  padding: 10px;
  background-color: #f0f0f0; /* Couleur de fond des messages */
  border-radius: 5px;
  margin-top: 20px;
}

/* Style pour la zone de saisie de messages */
.message-input {
  display: flex;
  align-items: center;
  margin-top: 20px;
}

.message-input button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.message-input button:hover {
  background-color: #0056b3;
}

/* Ajout d'icônes emoji personnalisées */
.emoji {
  font-size: 24px;
  margin-right: 5px;
}
</style>