function FlipperFeature() {
    var self = this;

    this.name = null;
    this.flipped = null;
    this.unflipped = null;

    this.doCheck = function(context, done){
        done(false);
    };

    this.setCheck = function(v){
        self.doCheck = v;
        return self;
    };

    this.setName = function(v){
        self.name = v;
        return self;
    };

    this.setFlipped = function(v){
        self.flipped = v;
        return self;
    };

    this.setUnflipped = function(v){
        self.unflipped = v;
        return self;
    };

    this.check = function(context, done) {
        self.doCheck(context, function(answer){
            if(typeof done === 'function') {
                done(answer === true ? self.flipped : self.unflipped);
            }
        });
    };
}

function Flipper() {
    var self = this;
    this.features = new Array();

    this.register = function(name) {
        var feature = new FlipperFeature()
                            .setName(name);
        self.features.push(feature);
        return feature;
    };

    this.get = function(name) {
        var feature = null;

        for(var i = 0; i < self.features.length; i++) {
            var f = self.features[i];
            if(f.name === name) {
                feature = f;
                break;
            }
        }

        return feature;
    };

}

if(typeof module !== 'undefined') {
    module.exports = new Flipper;
} else if(typeof window !== 'undefined') {
    window.flipper = new Flipper;
}
