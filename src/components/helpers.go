package auth_gateway

import (
	"crypto/rand"
	"encoding/base64"
	"log"
	"time"

	"github.com/dgrijalva/jwt-go"
)

func GenerateToken(user_id int, TokenType string) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"exp": time.Now().Add(time.Hour * 72).Unix(),
		"iat": time.Now().Unix(),
		"sub": user_id,
		"typ": TokenType,
	})

	signedToken, err := token.SignedString([]byte("secret-key"))
	if err != nil {
		log.Println(err)
		return "", err
	}
	return signedToken, nil
}

func ValidateToken(tokenString string) (*jwt.Token, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
		}
		return []byte("secret-key"), nil
	})
	if err != nil {
		return nil, err
	}
	if token.Valid {
		return token, nil
	} else {
		return nil, errors.New("invalid token")
	}
}

func GenerateUUID() (string, error) {
	uuidBytes := make([]byte, 16)
	_, err := rand.Read(uuidBytes)
	if err != nil {
		return "", err
	}
	uuid := base64.URLEncode(uuidBytes)
	return uuid, nil
}