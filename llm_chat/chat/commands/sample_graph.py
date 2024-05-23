import logging

from streamlit_agraph import Config, Edge, Node, agraph

from llm_chat.chat.commands.base_command import ChatCommand

logger = logging.getLogger(__name__)


class SampleGraphCommand(ChatCommand):
    @classmethod
    def name(cls):
        return "sample_graph"

    @classmethod
    def llm_descriptor(cls) -> str:
        return """
        In the case of sample_graph, there should be no arguments in the LIST_OF_ARGS. 
        """

    @classmethod
    def examples(cls) -> list[str]:
        return ["sample_graph", "show sample graph", "sample graph"]

    @classmethod
    def expected_params(cls) -> list[str]:
        return [""]

    def execute(self, my_bar) -> bool:
        nodes = []
        edges = []

        s = Node(
            id="Spiderman", label="Peter Parker", size=25, shape="circularImage", image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png"
        )
        m = Node(id="Captain_Marvel", size=25, shape="circularImage", image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png")
        c = Node(id="aaa", size=25, shape="circularImage", image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png")
        nodes.append(s)  # includes **kwargs
        nodes.append(m)
        nodes.append(c)
        edges.append(
            Edge(
                source="Captain_Marvel",
                label="friend_of",
                target="Spiderman",
                # **kwargs
            )
        )
        edges.append(
            Edge(
                source="Captain_Marvel",
                label="friend_of",
                target="aaa",
                # **kwargs
            )
        )
        edges.append(
            Edge(
                source="aaa",
                label="friend_of",
                target="Spiderman",
                # **kwargs
            )
        )

        config = Config(
            width=750,
            height=950,
            directed=True,
            physics=True,
            hierarchical=False,
            # **kwargs
        )

        agraph(nodes=nodes, edges=edges, config=config)
        return True
