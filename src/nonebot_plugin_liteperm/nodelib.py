class Node:
    data:dict[str,dict[str,dict|bool]]
    node_list:list[str]
    def __init__(self,data:dict,node:str=""):
        self.data=data["nodes"]
        self.node_list=node.split(".")
    
    @property
    def nodes(self)->dict:
        return self.data

    def set_value(self,n_value:bool):
        node_list=self.node_list
        data=self.data
        dict_tmp=data
        for index, value in enumerate(node_list):
            if index == len(node_list)-1:
                if value == "*":
                    dict_tmp["__all__"]=n_value
                else:
                    dict_tmp[value]["__has__"]=n_value
            elif dict_tmp.get(value):
                dict_tmp=dict_tmp[value]
            else:
                dict_tmp[value]={
                "__has__":True,
                "__all__":False,
            }
                dict_tmp=dict_tmp[value]
    
    def has(self)->bool:
        data=self.data
        node_list=self.node_list
        dict_tmp=data
        for index,value in enumerate(node_list):
            if isall :=dict_tmp.get("__all__"):
                return True
            elif isall is None:
                dict_tmp["__all__"]=False
            if index==len(node_list)-1:
                if value in dict_tmp:
                    if has:=(dict_tmp[value]).get("__has__") is True:
                        return True
                    elif has is None:
                        dict_tmp[value]["__has__"]=True
                        return True
                    else:
                        return False
                elif dict_tmp.get(value):
                    dict_tmp=dict_tmp[value]
                else :
                    return False
        return False

