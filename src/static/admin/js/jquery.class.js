(function($) {

    /*
        Система классов Javascript.

        1) Если функция инициализации вернет false - это является сигналом
           ошибки инициализации.
        2) При ошибке иницилизации:
            а) если объект создавался через CLASS.create() - вызов вернет undefined
            б) если объект создавался через new CLASS() - вернет объект, но, вероятно, неполный.
        3) При наследовании функции инициализации не забываем, что родительская
           функция может вернуть false. В этом случае, нужно также вернуть false.
        4) Не путаем:
            родительский метод инициализации - superclass.init
            родительский метод METHOD        - superclass.prototype.METHOD


        Пример 1:
            // создание класса Point2D, унаследованного от Object
            // с функцией инициализации и методом print().

            var Point2D = Class(null, function(cls, superclass) {
                cls.init = function(x, y) {
                    this._x = parseInt(x);
                    if (isNaN(this._x)) {
                        console.error('invalid X');
                        return false;
                    }

                    this._y = parseInt(y);
                    if (isNaN(this._y)) {
                        console.error('invalid Y');
                        return false;
                    }
                }

                cls.prototype.print = function() {
                    return this._x + ':' + this._y
                }
            });

        Пример 2:
            // создание дочернего класса Point3D, унаследованного от Point2D.

            var Point3D = Class(Point2D, function(cls, superclass) {
                cls.init = function(x, y, z) {
                    if (superclass.init.call(this, x, y) === false) {
                        return false
                    }

                    this._z = parseInt(z);
                    if (isNaN(this._z)) {
                        console.error('invalid Z');
                        return false;
                    }
                }

                cls.prototype.print = function() {
                    return superclass.prototype.print.call(this) + ':' + this._z
                }
            });

        Пример 3:
            // создание экземпляров классов

            > Point2D.create()
            < invalid X
            < undefined

            > new Point2D()
            < invalid X
            < InnerFunc {_x:NaN, ...}

            > p2 = Point2D.create(6, 7)
            < Object {_x:6, _y:7, ...}

            > p3 = new Point3D(2, 3, 4)
            < InnerFunc {_x:2, _y:3, _z:4, ...}

            > p2.print()
            < "6:7"

            > p3.print()
            < "2:3:4"
     */

    window.Class = function(parent, constructor) {
        var InnerFunc = function() {
            this.__init_result = InnerFunc.init.apply(this, arguments);
        };

        // установка прототипа, унаследованного от родительского
        InnerFunc.prototype = Object.create(parent && parent.prototype);
        InnerFunc.prototype.constructor = InnerFunc;
        InnerFunc.superclass = parent;

        // конструктор класса, возвращающий undefined в случае, если
        // функция инициализации вернет false
        InnerFunc.create = function() {
            // вызов конструктора с хаком для .apply()
            var obj = Object.create(InnerFunc.prototype);
            InnerFunc.apply(obj, arguments);
            obj.constructor = InnerFunc;

            if (obj.__init_result === false) {
                return
            }

            return obj;
        };

        // вызов функции, добавляющей пользовательские методы и свойства
        constructor(InnerFunc, parent);

        // если метод инициализации не описан - ищем в родителе
        if (InnerFunc.init === undefined) {
            if (parent.init) {
                InnerFunc.init = parent.init;
            } else {
                console.error('Class has no "init" method');
            }
        }

        return InnerFunc;
    };

})(jQuery);