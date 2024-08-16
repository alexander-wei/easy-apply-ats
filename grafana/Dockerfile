FROM grafana/grafana

#COPY ./mysql_datasource.yml /usr/share/grafana/conf/provisioning/datasources/default.yaml

COPY ./mysql_datasource.yml /etc/grafana/provisioning/datasources/default.yaml
COPY ./dashboard.json /etc/grafana/provisioning/dashboards/dashboard.json
COPY ./dashboards.yaml /etc/grafana/provisioning/dashboards/default.yaml

COPY ./grafana.ini /etc/grafana/grafana.ini
