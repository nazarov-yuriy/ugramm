from flask import Flask, request, jsonify
from flasgger import Swagger
from libs.engines import EngineFactory

app = Flask(__name__)
swagger = Swagger(app)
engine_factory = EngineFactory()


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route("/api/v1/check", methods=["POST"])
def check():
    """
    Check text
    ---
    parameters:
      - name: engine
        in: query
        type: string
        default: dummy
      - name: body
        in: body
        schema:
          properties:
            text:
              type: string
          example:
            {"text": "Don't need a consolidation agreement so we don't have to negotiate one."}
    responses:
      200:
        description: Check results
    """
    engine = engine_factory.get_engine(request.args.get("engine"))
    return jsonify(engine.check(request.json["text"]).serialize())


app.run(debug=True)
