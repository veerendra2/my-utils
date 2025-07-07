package main

import (
	"fmt"
	"log"

	"github.com/distribution/reference"
)

const LatestTag = "latest"

type ImageSpec struct {
	Name      string
	Registry  string
	Tag       string
	IsPublic  bool
	Namespace string
}

var (
	imageStrings = []string{
		"ubuntu",
		"ubuntu:latest",
		"myregistry.com/my-app:v1.2.3",
		"some.registry:5000/path/to/image:tag",
		"ubuntu@sha256:4567... (truncated)", // Example with digest
		"docker.io/library/ubuntu:latest",   // Fully qualified Docker Hub image
		"my-app",                            // Short name, will default to docker.io/library/my-app
		"hello-world:foo",
	}
	publicRegistries = map[string]bool{
		"docker.io":      true,
		"quay.io":        true,
		"gcr.io":         true,
		"ghcr.io":        true,
		"public.ecr.aws": true,
	}
)

func main() {
	imagesSpecs := []ImageSpec{}

	for _, image := range imageStrings {
		parsedRef, err := reference.ParseNormalizedNamed(image)
		if err != nil {
			log.Printf("Error parsing '%s': %v\n", image, err)
			continue
		}
		tag := LatestTag
		registry := reference.Domain(parsedRef)
		isPublic := false

		if tagged, ok := parsedRef.(reference.NamedTagged); ok {
			tag = tagged.Tag()
		}
		if publicRegistries[registry] {
			isPublic = true
		}

		imagesSpecs = append(imagesSpecs, ImageSpec{
			Name:     reference.Path(parsedRef),
			Registry: registry,
			Tag:      tag,
			IsPublic: isPublic,
		})
	}
	fmt.Println(imagesSpecs)
}
