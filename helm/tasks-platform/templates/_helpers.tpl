{{/* Labels shared by every resource */}}
{{- define "tasks.labels" -}}
app.kubernetes.io/part-of: tasks-platform
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
environment: {{ .Values.environment | quote }}
{{- end }}

{{/* Selector labels for one component. Usage: include "tasks.selector" (dict "component" "backend") */}}
{{- define "tasks.selector" -}}
app.kubernetes.io/name: tasks-{{ .component }}
app.kubernetes.io/component: {{ .component }}
{{- end }}

{{/* Name of the Secret holding the database credentials */}}
{{- define "tasks.dbSecretName" -}}
{{- default "tasks-db-credentials" .Values.database.existingSecret -}}
{{- end }}

{{/* Database host: external (RDS) when set, otherwise the in-cluster StatefulSet service */}}
{{- define "tasks.dbHost" -}}
{{- if .Values.database.host -}}
{{- .Values.database.host -}}
{{- else -}}
postgres.{{ .Release.Namespace }}.svc.cluster.local
{{- end -}}
{{- end }}

{{/* Container security context that satisfies the "restricted" Pod Security Standard */}}
{{- define "tasks.containerSecurityContext" -}}
allowPrivilegeEscalation: false
capabilities:
  drop: ["ALL"]
{{- end }}
