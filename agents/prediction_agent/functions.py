import agentpy as ap
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
import matplotlib.pyplot as plt
import json

class ForestModel(ap.Model):

    def setup(self):

        n_trees = int(self.p['Tree density'] * (self.p.size**2))
        trees = self.agents = ap.AgentList(self, n_trees)

        self.forest = ap.Grid(self, [self.p.size]*2, track_empty=True)
        self.forest.add_agents(trees, random=True, empty=True)

        self.agents.condition = 0

        unfortunate_trees = self.forest.agents[0:self.p.size, 0:2]
        unfortunate_trees.condition = 1

    def step(self):

        burning_trees = self.agents.select(self.agents.condition == 1)

        for tree in burning_trees:
            for neighbor in self.forest.neighbors(tree):
                if neighbor.condition == 0:
                    neighbor.condition = 1 # Neighbor starts burning
            tree.condition = 2 # Tree burns out

        if len(burning_trees) == 0:
            self.stop()

    def end(self):

        # Document a measure at the end of the simulation
        burned_trees = len(self.agents.select(self.agents.condition == 2))
        self.report('Percentage of burned trees',
                    burned_trees / len(self.agents))

def animation_plot(model, ax):
    attr_grid = model.forest.attr_grid('condition')
    color_dict = {0:'#7FC97F', 1:'#d62c2c', 2:'#e5e5e5', None:'#d5e5d5'}
    ap.gridplot(attr_grid, ax=ax, color_dict=color_dict, convert=True)
    ax.set_title(f"Simulation of a forest fire\n"
                 f"Time-step: {model.t}, Trees left: "
                 f"{len(model.agents.select(model.agents.condition == 0))}")


def generate_animation(**parameters):


    fig, ax = plt.subplots()
    model = ForestModel(**parameters)
    animation = ap.animate(model, fig, ax, animation_plot)
    return animation



def upload_json_to_blob_storage(
    json_data: dict,
    blob_name: str,
    connection_string: str = None,
    container_name: str = "container-name"
) -> str:

    if connection_string is None:
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise ValueError
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(container_name)

        try:
            container_client.create_container()
            print(f"Contenedor '{container_name}' creado (si no existía).")
        except Exception as e:
            if "ContainerAlreadyExists" not in str(e):
                print(f"Advertencia al crear el contenedor (posiblemente ya existe): {e}")

        blob_client = container_client.get_blob_client(blob_name)

        json_string = json.dumps(json_data, indent=4) # indent=4 para una salida JSON legible

        blob_client.upload_blob(json_string, overwrite=True) # overwrite=True para reemplazar si ya existe


        return blob_client.url

    except Exception as e:
        print(f"Error al subir el JSON a Blob Storage: {e}")
        return ""