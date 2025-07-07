package kube

import (
	"context"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
)

type client struct {
	kubeClient kubernetes.Clientset
}

type Client interface {
	GetImagesFromCronJobs(ctx context.Context) (map[string]struct{}, error)
	GetImagesFromDaemonSets(ctx context.Context) (map[string]struct{}, error)
	GetImagesFromDeployments(ctx context.Context) (map[string]struct{}, error)
	GetImagesFromPods(ctx context.Context) (map[string]struct{}, error)
	GetImagesFromStatefulSets(ctx context.Context) (map[string]struct{}, error)
}

func (c *client) GetImagesFromCronJobs(ctx context.Context) (map[string]struct{}, error) {
	cronJobList, err := c.kubeClient.BatchV1().CronJobs("").List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, err
	}

	images := make(map[string]struct{})
	for _, cj := range cronJobList.Items {
		for _, container := range cj.Spec.JobTemplate.Spec.Template.Spec.Containers {
			images[container.Image] = struct{}{}
		}
		for _, initContainer := range cj.Spec.JobTemplate.Spec.Template.Spec.InitContainers {
			images[initContainer.Image] = struct{}{}
		}
	}
	return images, nil
}

func (c *client) GetImagesFromDaemonSets(ctx context.Context) (map[string]struct{}, error) {
	daemonSetList, err := c.kubeClient.AppsV1().DaemonSets("").List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, err
	}

	images := make(map[string]struct{})
	for _, ds := range daemonSetList.Items {
		for _, container := range ds.Spec.Template.Spec.Containers {
			images[container.Image] = struct{}{}
		}
		for _, initContainer := range ds.Spec.Template.Spec.InitContainers {
			images[initContainer.Image] = struct{}{}
		}
	}
	return images, nil
}

func (c *client) GetImagesFromPods(ctx context.Context) (map[string]struct{}, error) {
	podList, err := c.kubeClient.CoreV1().Pods("").List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, err
	}

	images := make(map[string]struct{})

	for _, pod := range podList.Items {
		for _, container := range pod.Spec.Containers {
			images[container.Image] = struct{}{}
		}
		for _, initContainer := range pod.Spec.InitContainers {
			images[initContainer.Image] = struct{}{}
		}
	}

	return images, nil
}

func (c *client) GetImagesFromDeployments(ctx context.Context) (map[string]struct{}, error) {
	deploymentList, err := c.kubeClient.AppsV1().Deployments("").List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, err
	}

	images := make(map[string]struct{})
	for _, deploy := range deploymentList.Items {
		for _, container := range deploy.Spec.Template.Spec.Containers {
			images[container.Image] = struct{}{}
		}
		for _, initContainer := range deploy.Spec.Template.Spec.InitContainers {
			images[initContainer.Image] = struct{}{}
		}
	}
	return images, nil
}

func (c *client) GetImagesFromStatefulSets(ctx context.Context) (map[string]struct{}, error) {
	statefulSetList, err := c.kubeClient.AppsV1().StatefulSets("").List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, err
	}

	images := make(map[string]struct{})
	for _, sts := range statefulSetList.Items {
		for _, container := range sts.Spec.Template.Spec.Containers {
			images[container.Image] = struct{}{}
		}
		for _, initContainer := range sts.Spec.Template.Spec.InitContainers {
			images[initContainer.Image] = struct{}{}
		}
	}
	return images, nil
}

func NewClient(Kubeconfig string) (Client, error) {
	var restConfig *rest.Config
	var err error

	if Kubeconfig != "" {
		restConfig, err = clientcmd.BuildConfigFromFlags("", Kubeconfig)
		if err != nil {
			return nil, err
		}
	} else {
		restConfig, err = rest.InClusterConfig()
		if err != nil {
			return nil, err
		}

	}

	clientset, err := kubernetes.NewForConfig(restConfig)
	if err != nil {
		return nil, err
	}

	return &client{
		kubeClient: *clientset,
	}, nil
}
