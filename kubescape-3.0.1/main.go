package main

import (
	logger "github.com/kubescape/go-logger"
	"github.com/kubescape/kubescape/v3/cmd"
)

func main() {
	if err := cmd.Execute(); err != nil {
		logger.L().Fatal(err.Error())
	}

}
