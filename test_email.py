from airflow.operators.email import EmailOperator

allowlist = ['smtp.adeo.no:26']
send_email = EmailOperator(
    task_id="send-email",
    to=[
      "email@gmail.com",
    ],
    cc=[
      "email@gmail.com",
    ],
    subject=f"Feil i konsument",
    html_content="""<p>Dagen feiler i konsument </p>""",
    dag=dag,
    executor_config = {
            "pod_override": k8s.V1Pod(
                metadata=k8s.V1ObjectMeta(annotations={"allowlist": ",".join(allowlist)})
            )
        }
)