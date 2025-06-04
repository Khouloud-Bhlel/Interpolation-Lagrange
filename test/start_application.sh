#!/bin/bash

# 🚀 Script de démarrage pour l'application d'animation d'interpolation de Lagrange
# Ce script démarre tous les services nécessaires

echo "🎯 Démarrage de l'application d'animation d'interpolation de Lagrange"
echo "=================================================================="

# Fonction pour vérifier si un service est en cours d'exécution
check_service() {
    local service_name=$1
    local port=$2
    
    if nc -z localhost $port >/dev/null 2>&1; then
        echo "✅ $service_name est déjà en cours d'exécution sur le port $port"
        return 0
    else
        echo "⏳ $service_name n'est pas encore accessible sur le port $port"
        return 1
    fi
}

# Vérifier si nous sommes dans le bon répertoire
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Erreur: docker-compose.yml non trouvé. Assurez-vous d'être dans le répertoire lagrange_animator"
    exit 1
fi

echo "📁 Répertoire de travail: $(pwd)"

# 1. Démarrer les services Docker
echo ""
echo "🐳 Démarrage des services Docker (Odoo + PostgreSQL)..."
docker-compose up -d

# Attendre que les services Docker soient prêts
echo "⏳ Attente du démarrage des services Docker..."
sleep 10

# Vérifier PostgreSQL
while ! check_service "PostgreSQL" 5432; do
    echo "   Attente de PostgreSQL..."
    sleep 5
done

# Vérifier Odoo
while ! check_service "Odoo" 8069; do
    echo "   Attente d'Odoo..."
    sleep 5
done

echo "✅ Services Docker démarrés avec succès!"

# 2. Activer l'environnement virtuel Python
echo ""
echo "🐍 Activation de l'environnement Python..."
if [ -f "lagrange_env/bin/activate" ]; then
    source lagrange_env/bin/activate
    echo "✅ Environnement virtuel activé"
else
    echo "❌ Environnement virtuel non trouvé. Création en cours..."
    python3 -m venv lagrange_env
    source lagrange_env/bin/activate
    pip install -r requirements.txt
    echo "✅ Environnement virtuel créé et configuré"
fi

# 3. Vérifier les migrations Django
echo ""
echo "🔧 Vérification des migrations Django..."
python manage.py makemigrations --check --dry-run > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Migrations Django à jour"
else
    echo "⏳ Application des migrations Django..."
    python manage.py makemigrations
    python manage.py migrate
fi

# 4. Démarrer le serveur Django
echo ""
echo "🌐 Démarrage du serveur Django..."
echo "⏳ Le serveur sera disponible sur http://127.0.0.1:8000/"

# Vérifier si le port 8000 est libre
if check_service "Django" 8000; then
    echo "⚠️  Le port 8000 est déjà utilisé. Arrêt du serveur existant..."
    pkill -f "manage.py runserver"
    sleep 2
fi

# Démarrer le serveur en arrière-plan
nohup python manage.py runserver > django.log 2>&1 &
DJANGO_PID=$!

# Attendre que Django soit prêt
echo "⏳ Attente du démarrage du serveur Django..."
for i in {1..30}; do
    if check_service "Django" 8000; then
        break
    fi
    sleep 1
done

if check_service "Django" 8000; then
    echo "✅ Serveur Django démarré avec succès!"
else
    echo "❌ Échec du démarrage du serveur Django"
    exit 1
fi

# 5. Exécuter les tests
echo ""
echo "🧪 Exécution des tests de fonctionnalité..."
python3 test_complete_functionality.py

# 6. Afficher les informations de connexion
echo ""
echo "=================================================================="
echo "🎉 Application démarrée avec succès!"
echo "=================================================================="
echo ""
echo "📋 Informations de connexion:"
echo "  🌐 Interface Web:     http://127.0.0.1:8000/"
echo "  🐘 Interface Odoo:    http://localhost:8069/"
echo "     └── Utilisateur:   admin"
echo "     └── Mot de passe:  admin123"
echo ""
echo "📡 API Endpoints:"
echo "  🧮 Interpolation:     POST http://127.0.0.1:8000/api/interpolate/"
echo "  🔄 Intégration Odoo:  POST http://127.0.0.1:8000/api/odoo/send/"
echo ""
echo "🎮 Utilisation:"
echo "  1. Accédez à l'interface web"
echo "  2. Saisissez un degré polynomial (1-10)"
echo "  3. Cliquez sur 'Générer l'Animation'"
echo "  4. Observez les 6 étapes d'animation"
echo "  5. Les données sont automatiquement synchronisées avec Odoo"
echo ""
echo "🛑 Pour arrêter l'application:"
echo "  • Serveur Django: kill $DJANGO_PID"
echo "  • Services Docker: docker-compose down"
echo ""
echo "📝 Logs Django: tail -f django.log"
echo "=================================================================="
