from flask import Flask, request, jsonify

from controlers.orchestrator import Orchestrator


class Api:
    def __init__(self, app: Flask, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.app = app

        self.orchestrator.start_monitoring()

        self.app.add_url_rule('/state/colors', 'setColors', self.set_colors,
                              methods=['GET'])
        self.app.add_url_rule('/state/brightness/<int:brightness>', 'setBrightness', self.set_brightness,
                              methods=['POST'])
        self.app.add_url_rule('/state/autoled', 'autoLed', self.set_auto_led,
                              methods=['POST'])
        self.app.add_url_rule('/state/addressed', 'addressedProperties', self.set_addressed_direction,
                              methods=['POST'])
        self.app.add_url_rule('/state/autoled/properties', 'autoledProperties', self.set_auto_led_properties,
                              methods=['POST'])
        self.app.add_url_rule('/state/sensors', 'sensorsState', self.set_monitoring,
                              methods=['POST'])
        self.app.add_url_rule('/state/animations/<int:number>', 'setAnimations', self.set_animations,
                              methods=['POST'])

    def set_colors(self):
        """
        Required query params:
        'r', 'g', 'b'
        """
        red = int(request.args['r'])
        green = int(request.args['g'])
        blue = int(request.args['b'])
        self.orchestrator.set_colors([red, green, blue])
        return jsonify({})

    def set_brightness(self, brightness):
        self.orchestrator.set_strip_brightness(brightness)
        return jsonify({})

    def set_auto_led(self):
        """
        Required query params:
        'enable'
        """
        if request.args.get('enable') == 'true' or request.args.get('enable') == 'True':
            self.orchestrator.start_auto_led()
        else:
            self.orchestrator.stop_auto_led()
        return jsonify({})

    def set_addressed_direction(self):
        """
        optional query params:
        'direction', 'frequency', 'count'
        """
        d = {}
        for key in request.args:
            d[key] = int(request.args[key])
        self.orchestrator.set_addressed_properties(d)
        return jsonify({})

    def set_auto_led_properties(self):
        """
        optional query params:
        'sensitivity', 'inertia', 'frequency', 'fade_speed'
        """
        d = {}
        for key in request.args:
            d[key] = int(request.args[key])
        self.orchestrator.set_autoled_properties(d)
        return jsonify({})

    def set_monitoring(self):
        """
        /state/sensors
        optional query params:
        'enable', 'timeout'
        """
        if request.args.__contains__('enable'):
            state = True if request.args.get('enable') == 'true' or request.args.get('enable') == 'True' else False
            if state:
                self.orchestrator.start_monitoring()
            else:
                self.orchestrator.stop_monitoring()
        if request.args.__contains__('timeout'):
            self.orchestrator.set_motion_timeout(int(request.args['timeout']))
        return jsonify({})

    def set_animations(self, number: int):
        if request.args.__contains__('speed'):
            self.orchestrator.set_animation_speed(int(request.args['speed']))
        self.orchestrator.set_animation(number)
        return jsonify({})
