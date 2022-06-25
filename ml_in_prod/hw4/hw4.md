В каждом пункте, кроме 0 и 1, вам потребуется поднятый Kubernetes кластер и утилита, которая помогает с ним взаимодействовать (https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

Для удобства управления ресурсами k8s можно установить [Lens](https://k8slens.dev/)

**Основная часть:**

0. Установите `kubectl`
1. Разверните Kubernetes (5 баллов)

   Вы можете развернуть его в облаке:
   - https://cloud.google.com/kubernetes-engine
   - https://mcs.mail.ru/containers/
   - https://cloud.yandex.ru/services/managed-kubernetes

   Либо воспользоваться локальной инсталляцией:
   - https://kind.sigs.k8s.io/docs/user/quick-start/
   - https://minikube.sigs.k8s.io/docs/start/

   Напишите, какой способ вы выбрали (приложите скрины).

   Убедитесь, что кластер поднялся:
   ```bash
   kubectl cluster-info
   ```

2. Напишите простой [Pod manifest](https://kubernetes.io/docs/concepts/workloads/pods/) для вашего приложения, назовите его `online-inference-pod.yaml` (4 балла)

   Задеплойте приложение в кластер:
   ```bash
   kubectl apply -f online-inference-pod.yaml
   ```
   Убедитесь, что все поднялось:
   ```bash
   kubectl get pods
   ```
   Приложите скриншот, где видно, что все поднялось

3. Пропишите Requests / Limits и напишите, зачем это нужно в описании PR. Закоммитьте файл `online-inference-pod-resources.yaml` (2 балла)

4. Модифицируйте свое приложение так, чтобы оно стартовало не сразу (с задержкой 20-30 секунд) и падало спустя минуты работы. Добавьте Liveness и Readiness пробы и посмотрите, что будет происходить.
   Напишите в описании -- чего вы этим добились. Закоммитьте отдельный манифест `online-inference-pod-probes.yaml` (и изменение кода приложения). Опубликуйте ваше приложение (из ДЗ #2) с тэгом `v2` (3 балла)

5. Создайте [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/), сделайте 3 реплики вашего приложения. Закоммитьте `online-inference-replicaset.yaml` (3 балла)

   Ответьте на вопрос, что будет, если сменить docker образ в манифесте и одновременно с этим:

   a) уменьшить число реплик

   б) увеличить число реплик

   Поды с какими версиями образа будут внутри кластера?

6. Опишите [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) для вашего приложения (3 балла)
   Играя с параметрами деплоя (`maxSurge`, `maxUnavaliable`), добейтесь ситуации, когда при деплое новой версии:

   a) есть момент времени, когда на кластере существуют как все старые поды, так и все новые (опишите эту ситуацию) (закоммитьте файл `online-inference-deployment-blue-green.yaml`)

   б) одновременно с поднятием новых версий, гасятся старые (закоммитьте файл `online-inference-deployment-rolling-update.yaml`)

**Бонусные активности:**

7. Установите Helm и оформите Helm chart. Включите в состав чарта `ConfigMap` и `Service` (+5 доп баллов)
8. Разверните kubernetes кластер с помощью terraform (+5 доп баллов), закоммитьте terraform скрипты и инструкцию по использованию.
Материалы:
   - https://mcs.mail.ru/docs/networks/vnet/networks/tf-quick-start
   - https://cloud.yandex.ru/docs/tutorials/infrastructure-management/terraform-quickstart
   - https://kb.selectel.ru/docs/cloud/servers/tools/use-terraform/

**Процедура сдачи**:

После выполнения ДЗ создаем пулл реквест, в ревьюеры добавляем  Mikhail-M, ждем комментариев (на которые нужно ответить) и/или оценки.
Ветка должна называться _homework4_.

Пожалуйста добавьте к своему пулл реквесту метку _hw4_. Если вы студент MADE, то дополнительно укажите тэг -- _MADE_, если вы студент Технопарка -- тэг _TECHNOPARK_.

**Сроки выполнения**:

Мягкий дедлайн: **26 июня 23:59**

Жесткий дедлайн:  **29 июня 23:59**

**Важно:** после мягкого дедлайна все полученные баллы умножаются на 0.6

