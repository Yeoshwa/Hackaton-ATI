#!/bin/bash

API_URL="http://127.0.0.1:8000/api"
LOG_FILE="api_test.log"
echo "" > $LOG_FILE  # Vide le fichier de log au début

log() {
  echo -e "$1" | tee -a $LOG_FILE
}

log "Registering user..."
curl -s -X POST "$API_URL/register/" -H "Content-Type: application/json" -d '{"username":"testuser","email":"testuser@example.com","password":"TestPass123"}' | tee -a $LOG_FILE
log "\n"

log "Logging in..."
TOKEN=$(curl -s -X POST "$API_URL/login/" -H "Content-Type: application/json" -d '{"username":"testuser","password":"TestPass123"}' | tee -a $LOG_FILE | python -c "import sys, json; print(json.load(sys.stdin)['access'])")
log "Token: $TOKEN\n"

log "Getting profile..."
curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/profile/" | tee -a $LOG_FILE
log "\n"

log "Getting leaderboard..."
curl -s "$API_URL/users/leaderboard/" | tee -a $LOG_FILE
log "\n"

log "Creating report..."
REPORT_ID=$(curl -s -X POST "$API_URL/reports/" -H "Authorization: Bearer $TOKEN" -F "latitude=48.85" -F "longitude=2.35" -F "description=Test report" -F "statut=signale" -F "gravite=1" -F "photo=@test.jpg" | tee -a $LOG_FILE | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
log "Report ID: $REPORT_ID\n"

log "Listing reports..."
curl -s "$API_URL/reports/" | tee -a $LOG_FILE
log "\n"

log "Getting report detail..."
curl -s "$API_URL/reports/$REPORT_ID/" | tee -a $LOG_FILE
log "\n"

log "Adding comment..."
curl -s -X POST "$API_URL/reports/$REPORT_ID/comments/" -H "Authorization: Bearer $TOKEN" -d "content=Bravo pour le signalement" | tee -a $LOG_FILE
log "\n"

log "Listing comments..."
curl -s "$API_URL/reports/$REPORT_ID/comments/" | tee -a $LOG_FILE
log "\n"

log "Deleting report..."
curl -s -X DELETE "$API_URL/reports/$REPORT_ID/" -H "Authorization: Bearer $TOKEN" | tee -a $LOG_FILE
log "\n"

log "API test script finished."