from dataclasses import dataclass

@dataclass(slots=True)
class FlowStepLink:
    target:str
#加slots和不加的区别是，不加的话，创建一个对象，里面的属性是__dict__的形式保存的
#也就是一个字典，那么创建完了后，还可以任意加属性，因为本质就是在往字典里面加字段以及值，
#但是如果是加了slots，那么属性就是真的以属性保存在对象里面了，那么创建了对象后就不可以再加新的属性了

@dataclass(slots=True)
class StaticLink(FlowStepLink):
    pass

@dataclass(slots=True)
class ConditionalLink(FlowStepLink):
    condition:str

@dataclass(slots=True)
class FallbackLink(FlowStepLink):
    pass
