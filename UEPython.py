import unreal
import sys

# Biliotecas e utilidades da Unreal
levelLib = unreal.EditorLevelLibrary
levelUtils = unreal.EditorLevelUtils
actorUtils = unreal.EditorActorSubsystem
stringUtils = unreal.StringLibrary
systemLib = unreal.SystemLibrary
assetLibrary = unreal.EditorAssetLibrary
dataTableLibrary = unreal.DataTableFunctionLibrary
dataSmithLibrary = unreal.DatasmithContentLibrary
arrayLibrary = unreal.KismetArrayLibrary

# Prefixos das tags
prefixTarefa = 'AYTF_'
prefixOrdem = 'AYOR_'
prefixQuantidade = 'AYQT_'

# Mapeamento das coordenadas
mapeamento = {"x": 0, "y": 1, "z": 2}

# region CLASSES


class Tarefa:
    def __init__(self, tarefa, dataInicialTarefa, dataFinalTarefa, animacao, materialEfeito, tempoInicialDaTarefa, tempoFinalTarefa):
        self.tarefa = tarefa
        self.dataInicialTarefa = dataInicialTarefa
        self.dataFinalTarefa = dataFinalTarefa
        self.animacao = animacao
        self.materialEfeito = materialEfeito
        self.tempoInicialDaTarefa = tempoInicialDaTarefa
        self.tempoFinalTarefa = tempoFinalTarefa

# endregion

# region FUNÇÕES


def CriarTagComBaseNaMetadataFBXB():

    print('CriarTagComBaseNaMetadataFBX')

    # Prefixos das tags
    prefixTarefa = 'AYTF_'
    prefixOrdem = 'AYOR_'
    prefixQuantidade = 'AYQT_'

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Endereço dos assets onde será procurado
    assetPath = '/Game/Meshes/LON_Unimed'

    # Pega os assets presentes no edereço
    assetRegistryHelper = unreal.AssetRegistryHelpers.get_asset_registry()
    assetRegistry = assetRegistryHelper.get_assets_by_path(
        assetPath, False, False)

    # Cria um dicionário com todos os assets e seus nomes como chaves
    dictAssetsNames = dict()
    for registry in assetRegistry:
        asset = registry.get_asset()
        assetName = systemLib.get_object_name(asset)
        dictAssetsNames[assetName] = asset

    # Para cada ator selecionado pega o seu asset correspondente
    for actor in selectedActors:
        if actor.__class__ == unreal.StaticMeshActor:
            components = actor.get_components_by_class(
                unreal.StaticMeshComponent)
            for component in components:
                componentName = systemLib.get_display_name(
                    component).split(' ')[1]
                componentAsset = dictAssetsNames[componentName]
                # Caso tenha um componentAsset com o nome correspondente pegar as informações do mesmo
                # e criar tags no Actor com base neles
                if componentAsset is not None:
                    tagValues = assetLibrary.get_metadata_tag_values(
                        componentAsset)
                    tarefa = tagValues.get('FBX.Element_AY_Tarefa')
                    ordem = tagValues.get('FBX.Element_AY_OrdemNaTarefa')
                    quantidade = tagValues.get(
                        'FBX.Element_AY_QuantidadeNaTarefa')

                    # Cria as tags no Actor com base no elemento na metadata do asset
                    # Também checa se já existe uma tag no elemento que inicia com o mesmo prefixo
                    actorTags = actor.tags
                    actorTagsString = []
                    for tag in actorTags:
                        actorTagsString.append(str(tag))

                    CriarTag(prefixTarefa, tarefa, actorTagsString, actorTags)
                    CriarTag(prefixOrdem, ordem, actorTagsString, actorTags)
                    CriarTag(prefixQuantidade, quantidade,
                             actorTagsString, actorTags)
        else:
            print('Ator selecionado não é um StaticMeshActor')


def CriarTagComBaseNaMetadataFBX():

    print('CriarTagComBaseNaMetadataFBX')

    # Prefixos das tags
    prefixTarefa = 'AYTF_'
    prefixOrdem = 'AYOR_'
    prefixQuantidade = 'AYQT_'

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Para cada ator selecionado pega o seu asset correspondente
    for actor in selectedActors:
        if actor.__class__ == unreal.StaticMeshActor:
            components = actor.get_components_by_class(
                unreal.StaticMeshComponent)
            for component in components:
                meshComponent = unreal.StaticMeshComponent.cast(component)
                componentPath = unreal.StructBase.to_tuple(
                    unreal.SystemLibrary.get_soft_object_path(meshComponent.static_mesh))
                componentAsset = unreal.load_object(
                    name=componentPath[0], outer=None)

                # Caso tenha um componentAsset pegar as informações do mesmo e criar tags no Actor com base neles
                if componentAsset is not None:
                    tagValues = assetLibrary.get_metadata_tag_values(
                        componentAsset)
                    tarefa = tagValues.get('FBX.Element_AY_Tarefa')
                    ordem = tagValues.get('FBX.Element_AY_OrdemNaTarefa')
                    quantidade = tagValues.get(
                        'FBX.Element_AY_QuantidadeNaTarefa')

                    # Cria as tags no Actor com base no elemento na metadata do asset
                    # Também checa se já existe uma tag no elemento que inicia com o mesmo prefixo
                    actorTags = actor.tags
                    actorTagsString = []
                    for tag in actorTags:
                        actorTagsString.append(str(tag))

                    CriarTag(prefixTarefa, tarefa, actorTagsString, actorTags)
                    CriarTag(prefixOrdem, ordem, actorTagsString, actorTags)
                    CriarTag(prefixQuantidade, quantidade,
                             actorTagsString, actorTags)
        else:
            print('Ator selecionado não é um StaticMeshActor')


def CriarTagComBaseNaMetadataDataTable():

    print('CriarTagComBaseNaMetadataDataTable')

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Pega todos os elementos que contém a chave Element_AY_Tarefa na sua metadata
    AdicionarTagPorMetadata('Element_AY_Tarefa', prefixTarefa)
    AdicionarTagPorMetadata('Element_AY_QuantidadeNaTarefa', prefixQuantidade)
    AdicionarTagPorMetadata('Element_AY_OrdemNaTarefa', prefixOrdem)


def LimparTagsAY():

    print('LimparTagsAY')
    
    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()
    
    # Para cada ator selecionado pegar as suas tags
    for actor in selectedActors:
        actorTags = actor.tags
        print(len(actorTags))
        for tag in reversed(actorTags):
            if str(tag).startswith(prefixTarefa):
                actorTags.remove(tag)
            if str(tag).startswith(prefixOrdem):
                actorTags.remove(tag)
            if str(tag).startswith(prefixQuantidade):
                actorTags.remove(tag)


def CriarLevelSequenceTracks(dataTable, dataInicial, dataFinal, usedate, usefirstlastdate):

    dataInicial = dataInicial
    dataFinal = dataFinal

    if usedate:

        # Calcula as datas iniciais e finais do cronograma
        dataInicial, dataFinal = CalcularDatasIniciaisEFinais(
            dataTable, usefirstlastdate)

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))
    elif usefirstlastdate:

        # Calcula as datas iniciais e finais do cronograma
        dataInicial, dataFinal = CalcularDatasIniciaisEFinais(
            dataTable, usefirstlastdate)

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))
    else:
        # Converte as datas de string dd/mm/yyyy para DataTimeStructure da Unreal
        arrDataInicial = unreal.StringLibrary.parse_into_array(
            dataInicial, "/", False)
        arrDataFinal = unreal.StringLibrary.parse_into_array(
            dataFinal, "/", False)

        dataInicial = "{0}-{1}-{2}-12.00.00".format(
            arrDataInicial[2], arrDataInicial[1], arrDataInicial[0])
        dataFinal = "{0}-{1}-{2}-12.00.00".format(
            arrDataFinal[2], arrDataFinal[1], arrDataFinal[0])

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))

        dataInicial = unreal.MathLibrary.date_time_from_string(dataInicial)
        dataFinal = unreal.MathLibrary.date_time_from_string(dataFinal)

    # Pega a LevelSequence que esta aberta
    levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Calcula o tempo base da sequence
    tempoTotalSequence = levelSequence.get_playback_end_seconds()
    diasTotais = CalcularDiasTotais(dataInicial, dataFinal)
    print('Dias totais: ' + str(diasTotais))
    sequenceFrameRate = levelSequence.get_display_rate()

    # Pega o LevelSequenceEditorSubSystem
    editorSubsystem = unreal.get_editor_subsystem(
        unreal.LevelSequenceEditorSubsystem)

    # Pega as colunas da DataTable
    dataTableColumns = PegarDadosDataTableCronograma(dataTable)

    # Caso tenham colunas
    if len(dataTableColumns) > 0:
        # Para cada coluna
        for i in range(len(dataTableColumns[0])):

            tarefa = prefixTarefa + \
                str(dataTableColumns[0][i])  # Nome da tarefa
            dataInicialTarefa = unreal.MathLibrary.date_time_from_string(
                dataTableColumns[1][i])
            dataFinalTarefa = unreal.MathLibrary.date_time_from_string(
                dataTableColumns[2][i])
            animacao = dataTableColumns[4][i]
            materialEfeito = unreal.load_object(
                name=dataTableColumns[3][i], outer=None)

            tempoInicialDaTarefa = CalcularTempoInicialDaTarefa(
                tempoTotalSequence, diasTotais, dataInicial, dataInicialTarefa)
            tempoFinalTarefa = CalcularTempoFinalDaTarefa(
                tempoTotalSequence, diasTotais, dataInicial, dataFinalTarefa)

            # Pega todos os atores com a tag
            actorsWithTag = unreal.GameplayStatics.get_all_actors_of_class_with_tag(
                selectedActors[0], unreal.StaticMeshActor, tarefa)

            # Filtra para apenas os selecionados
            actorsSelecionados = []
            for actor in actorsWithTag:
                if actor in selectedActors:
                    actorsSelecionados.append(actor)

            actorsWithTag = actorsSelecionados
            # print('Existem ' + str(len(actorsWithTag)) + ' Atores com a TAG ' + str(tarefa))

            # Cria um Array com o primeiro ator caso existam atores com a tag
            if len(actorsWithTag) > 0:

                # Cria um Array com o primeiro ator
                firstActorArray = [actorsWithTag[0]]

                # Calcula os tempos em FRAMES
                inicio = unreal.MathLibrary.round(
                    tempoInicialDaTarefa*sequenceFrameRate.numerator)
                fim = unreal.MathLibrary.round(
                    tempoFinalTarefa*sequenceFrameRate.numerator)
                frameInicial = unreal.FrameNumber(inicio)
                frameFinal = unreal.FrameNumber(fim)
                frameAntesDoInicial = unreal.FrameNumber(inicio-1)
                frameAposOFinal = unreal.FrameNumber(fim+1)

                # Pega o LevelSequenceEditorSubSystem
                editorSubsystem = unreal.get_editor_subsystem(
                    unreal.LevelSequenceEditorSubsystem)

                # Adiciona o primeiro ator a Sequence
                # actorTrack = editorSubsystem.add_actors(firstActorArray)

                # Adiciona o primeiro componente do ator como uma track
                actorComponent = firstActorArray[0].get_component_by_class(
                    unreal.StaticMeshComponent)
                componentBinding = levelSequence.add_possessable(
                    actorComponent)

                # Pega os novos outros componentes caso existam
                print(actorComponent)

                CriarTrackVisibilidade(componentBinding, frameAntesDoInicial, frameInicial)

                CriarTrackTrocaDeMateriais(
                    componentBinding, actorComponent, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal)

                CriarTrackParametroDeMaterial(
                    componentBinding, frameInicial, frameFinal)

                if animacao == "Montagem":
                    CriarTrackMoverElementoEmZ(
                        actor, componentBinding, frameInicial, frameFinal)

                # Adiciona todos os atores com a mesma TAG a track
                editorSubsystem.add_actors_to_binding(
                    actorsWithTag, componentBinding.get_parent())

                # Renomeia a track
                componentBinding.get_parent().set_display_name(
                    str(dataTableColumns[0][i]))
    else:
        print('Nenhum dado encontrado na DataTable')


def CriarLevelSequenceTracksOnlyVisibility(dataTable, dataInicial, dataFinal, usedate, usefirstlastdate):

    dataInicial = dataInicial
    dataFinal = dataFinal

    if usedate:

        # Calcula as datas iniciais e finais do cronograma
        dataInicial, dataFinal = CalcularDatasIniciaisEFinais(
            dataTable, usefirstlastdate)

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))
    elif usefirstlastdate:

        # Calcula as datas iniciais e finais do cronograma
        dataInicial, dataFinal = CalcularDatasIniciaisEFinais(
            dataTable, usefirstlastdate)

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))
    else:
        # Converte as datas de string dd/mm/yyyy para DataTimeStructure da Unreal
        arrDataInicial = unreal.StringLibrary.parse_into_array(
            dataInicial, "/", False)
        arrDataFinal = unreal.StringLibrary.parse_into_array(
            dataFinal, "/", False)

        dataInicial = "{0}-{1}-{2}-12.00.00".format(
            arrDataInicial[2], arrDataInicial[1], arrDataInicial[0])
        dataFinal = "{0}-{1}-{2}-12.00.00".format(
            arrDataFinal[2], arrDataFinal[1], arrDataFinal[0])

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))

        dataInicial = unreal.MathLibrary.date_time_from_string(dataInicial)
        dataFinal = unreal.MathLibrary.date_time_from_string(dataFinal)

    # Pega a LevelSequence que esta aberta
    levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()
    print('Existem ' + str(len(selectedActors)) + ' Atores selecionados')

    # Calcula o tempo base da sequence
    tempoTotalSequence = levelSequence.get_playback_end_seconds()
    diasTotais = CalcularDiasTotais(dataInicial, dataFinal)
    print('Dias totais: ' + str(diasTotais))
    sequenceFrameRate = levelSequence.get_display_rate()

    # Pega o LevelSequenceEditorSubSystem
    editorSubsystem = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)

    # Pega as colunas da DataTable
    dataTableColumns = PegarDadosDataTableCronograma(dataTable)

    # Filtra os objetos caso sejam Decals
    simpleActors = []
    decalActors = []

    for selectedActor in selectedActors:
        if type(selectedActor) == unreal.DecalActor:
            decalActors.append(selectedActor)
        else:
            simpleActors.append(selectedActor)
    
    # Cria um dicionário com as Tags referentes
    print('Criação dos dicionários')
    decalDictionary =  {}
    simpleDictionary = {}

    if len(decalActors) > 0:
        for decal in decalActors:
            decalComponent = decal.get_components_by_class(unreal.DecalComponent)[0]
            if len(decalComponent.component_tags) > 0:
                for tag in decalComponent.component_tags:
                    tag = str(tag)
                    if tag.startswith('AYTF'):
                    # Verifica se já existe a tag no dicionário
                        if tag in decalDictionary:
                            decalDictionary[tag].append(decal)
                        else:
                            decalDictionary[tag] = [decal]
    print(decalDictionary)

    if len(simpleActors) > 0:
        for simpleActor in simpleActors:
            if len(simpleActor.tags) > 0:
                for tag in simpleActor.tags:
                    tag = str(tag)
                    if tag.startswith('AYTF'):
                    # Verifica se já existe a tag no dicionário
                        if tag in simpleDictionary:
                            simpleDictionary[tag].append(simpleActor)
                        else:
                            simpleDictionary[tag] = [simpleActor]
    
    print(simpleDictionary)    

    # Caso tenham colunas
    if len(dataTableColumns) > 0:
        # Para cada coluna
        for i in range(len(dataTableColumns[0])):

            tarefa = prefixTarefa + \
                str(dataTableColumns[0][i])  # Nome da tarefa
            dataInicialTarefa = unreal.MathLibrary.date_time_from_string(dataTableColumns[1][i])
            dataFinalTarefa = unreal.MathLibrary.date_time_from_string(dataTableColumns[2][i])
            animacao = dataTableColumns[4][i]
            materialEfeito = unreal.load_object(name=dataTableColumns[3][i], outer=None)

            tempoInicialDaTarefa = CalcularTempoInicialDaTarefa(tempoTotalSequence, diasTotais, dataInicial, dataInicialTarefa)
            tempoFinalTarefa = CalcularTempoFinalDaTarefa(tempoTotalSequence, diasTotais, dataInicial, dataFinalTarefa)

            # Calcula os tempos em FRAMES
            inicio = unreal.MathLibrary.round(tempoInicialDaTarefa*sequenceFrameRate.numerator)
            fim = unreal.MathLibrary.round(tempoFinalTarefa*sequenceFrameRate.numerator)
            frameInicial = unreal.FrameNumber(inicio)
            frameFinal = unreal.FrameNumber(fim)
            frameAntesDoInicial = unreal.FrameNumber(inicio-1)
            frameAposOFinal = unreal.FrameNumber(fim+1)

            if tarefa in simpleDictionary:
                actorsFromDictionary = simpleDictionary[tarefa]

                if len(actorsFromDictionary) > 0:
                    for actor in actorsFromDictionary:
                        componentBinding = levelSequence.add_possessable(actor)
                        CriarTrackVisibilidadeActor(componentBinding, frameAntesDoInicial, frameInicial)

            if tarefa in decalDictionary:
                print(tarefa)
                decalsFromDictionary = decalDictionary[tarefa]
                print(decalsFromDictionary)

                if len(decalsFromDictionary) > 0:
                    for decal in decalsFromDictionary:
                        componentBinding = levelSequence.add_possessable(decal)
                        CriarTrackVisibilidadeActor(componentBinding, frameAntesDoInicial, frameInicial)                 


        
                
            # if len(simpleActors) > 0:

            #     # Pega todos os atores com a tag
            #     actorsWithTag = unreal.GameplayStatics.get_all_actors_with_tag(simpleActors[0], tarefa)

            #     # Filtra para apenas os selecionados
            #     actorsSelecionados = []
            #     for actor in actorsWithTag:
            #         if actor in simpleActors:
            #             actorsSelecionados.append(actor)

            #     actorsWithTag = actorsSelecionados

            #     # Cria um Array com o primeiro ator caso existam atores com a tag
            #     if len(actorsWithTag) > 0:

            #         # Cria um Array com o primeiro ator
            #         firstActorArray = [actorsWithTag[0]]

            #         # Calcula os tempos em FRAMES
            #         inicio = unreal.MathLibrary.round(tempoInicialDaTarefa*sequenceFrameRate.numerator)
            #         fim = unreal.MathLibrary.round(tempoFinalTarefa*sequenceFrameRate.numerator)
            #         frameInicial = unreal.FrameNumber(inicio)
            #         frameFinal = unreal.FrameNumber(fim)
            #         frameAntesDoInicial = unreal.FrameNumber(inicio-1)
            #         frameAposOFinal = unreal.FrameNumber(fim+1)

            #         # Pega o LevelSequenceEditorSubSystem
            #         editorSubsystem = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)
                    
            #         componentBinding = levelSequence.add_possessable(firstActorArray[0])
            #         CriarTrackVisibilidadeActor(componentBinding, frameAntesDoInicial, frameInicial)

            # # Agora para os Decals
            # if len(decalActors) > 0:
            #     for decal in decalActors:
            #         print(decal)
            #         decalComponent = decal.get_components_by_class(unreal.DecalComponent)[0]
            #         if len(decalComponent.component_tags) > 0:
            #             if tarefa in decalComponent.component_tags:
            #                 componentBinding = levelSequence.add_possessable(decal)
            #                 CriarTrackVisibilidadeActor(componentBinding, frameAntesDoInicial, frameInicial)

   
    else:
        print('Nenhum dado encontrado na DataTable')


def RemoverStringDoNomeDoAsset(string):

    print('RemoverStringDoNomeDoAsset')

    # Pega os assets selectionados
    selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()

    # Salva no log
    unreal.log("Selecionados {} assets".format(len(selectedAssets)))
    replaced = 0

    # Para cada ator selecionado pegar as suas tags
    for asset in selectedAssets:
        assetName = unreal.SystemLibrary().get_object_name(asset)
        if unreal.StringLibrary.contains(assetName, string, use_case=False):
            newAssetName = unreal.StringLibrary.replace(assetName, string, "")
            unreal.EditorUtilityLibrary.rename_asset(asset, newAssetName)
            replaced += 1

    unreal.log("Foram alterados {} assets".format(replaced))


def PegarInformacoesDasTracks():

    print('PegarInformacoesDasTracks')

    # Pega a LevelSequence que esta aberta
    levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

    bindings = unreal.MovieSceneSequence.get_bindings(levelSequence)

    for bind in bindings:
        tracks = bind.get_tracks()
        for track in tracks:
            print(f"NOME DA TRACK: {track.get_display_name()}")
            print(track)
            sections = track.get_sections()
            for section in sections:
                print(section)
                channelsParameter = section.get_all_channels()
                for channel in channelsParameter:
                    print(channel)


def CriarLevelSequenceComplexTracks(dataTable, dataInicial, dataFinal, usedate, usefirstlastdate,
                                    coordenada_inicial="x", inverter_coordenada_inicial=False, coordenada_secundaria="y",
                                    inverter_coordenada_secundaria=False, tolerancia=100, dividirComponentes=False):

    # Calcular as datas do cronograma
    datas = CalcularDataInicialEFinal(
        dataTable, dataInicial, dataFinal, usedate, usefirstlastdate)

    dataInicial = datas[0]
    dataFinal = datas[1]

    # Pega a LevelSequence que esta aberta
    levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

    # Calcula o tempo base da sequence
    tempoTotalSequence = levelSequence.get_playback_end_seconds()
    diasTotais = CalcularDiasTotais(dataInicial, dataFinal)
    print('Dias totais: ' + str(diasTotais))
    sequenceFrameRate = levelSequence.get_display_rate()

    # Pega as colunas da DataTable
    dataTableColumns = PegarDadosDataTableCronograma(dataTable)

    # Cria a lista de objetos Tarefa
    tarefas = []

    if len(dataTableColumns) > 0:

        # Para cada linha das colunas colunas
        for i in range(len(dataTableColumns[0])):

            tarefa = prefixTarefa + str(dataTableColumns[0][i])  # Nome da tarefa
            dataInicialTarefa = unreal.MathLibrary.date_time_from_string(
                dataTableColumns[1][i])
            dataFinalTarefa = unreal.MathLibrary.date_time_from_string(
                dataTableColumns[2][i])
            animacao = dataTableColumns[4][i]
            materialEfeito = unreal.load_object(name= dataTableColumns[3][i], outer = None)
            tempoInicialDaTarefa = CalcularTempoInicialDaTarefa(
                tempoTotalSequence, diasTotais, dataInicial, dataInicialTarefa)
            tempoFinalTarefa = CalcularTempoFinalDaTarefa(
                tempoTotalSequence, diasTotais, dataInicial, dataFinalTarefa)

            tarefas.append(Tarefa(tarefa, dataInicialTarefa, dataFinalTarefa,
                           animacao, materialEfeito, tempoInicialDaTarefa, tempoFinalTarefa))

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Pega o LevelSequenceEditorSubSystem
    editorSubsystem = unreal.get_editor_subsystem(
        unreal.LevelSequenceEditorSubsystem)

    # Caso tenham colunas
    if len(dataTableColumns) > 0:

        # Para cada ator selecionado
        for actor in selectedActors:

            actorTags = actor.tags

            tarefaDoAtor = ""

            for tag in actorTags:
                tagString = unreal.StringLibrary.conv_name_to_string(tag)
                if tagString.startswith("AYTF_"):
                    tarefaDoAtor = tagString

            if tarefaDoAtor is not None:

                tarefaCronograma = next(
                    (tarefa for tarefa in tarefas if tarefa.tarefa == tarefaDoAtor), None)

                if tarefaCronograma is not None:

                    print('Tarefa do cronograma: ' + \
                          str(tarefaCronograma.tarefa))
                    print('Animação da tarefa ' + \
                          str(tarefaCronograma.animacao))

                    # Adiciona o primeiro componente do ator como uma track
                    actorComponents = actor.get_components_by_class(
                        unreal.StaticMeshComponent)

                    # Animação da tarefa
                    animacao = tarefaCronograma.animacao

                    # Material Efeito
                    materialEfeito = tarefaCronograma.materialEfeito

                    # Filtra os componentes pegando apenas aqueles que possuem mesh
                    componentesComMesh = []

                    for component in actorComponents:
                        print(component.get_name())
                        component = unreal.StaticMeshComponent.cast(component)
                        if unreal.SystemLibrary.is_valid(component.static_mesh):
                            componentesComMesh.append(component)

                    # Organiza os componentes de acordo com a posição

                    # Determina qual índice é correspondente a coordenada escolhida
                    coordenadaInicial = {"x": 0, "y": 1, "z": 2}[
                        coordenada_inicial]
                    coordenadaSecundaria = {"x": 0, "y": 1, "z": 2}[
                        coordenada_secundaria]
                    inverterCoordenadaInicial = inverter_coordenada_inicial
                    inverterCoordenadaSecundaria = inverter_coordenada_secundaria

                    coordenadasDosComponentes = PegarLocalizacaoDosComponentes(
                        componentesComMesh)

                    # print('COORDENADAS DOS COMPONENTES:')
                    # print(coordenadasDosComponentes)

                    coordenadasOrdenadas = AgruparEOrdenarPontosEmDuasCoordenadasComTolerancia(
                        coordenadasDosComponentes,
                        tolerancia,
                        tolerancia,
                        coordenadaInicial,
                        coordenadaSecundaria,
                        inverterCoordenadaInicial,
                        inverterCoordenadaSecundaria)

                    # print('COORDENADAS ORDENADAS:')
                    # print(coordenadasOrdenadas)

                    coordenadasPlanificadas = PlanificarListaDePontos(
                        coordenadasOrdenadas)

                    # print('COORDENADAS ORDENADAS PLANIFICADAS:')
                    # print(coordenadasPlanificadas)

                    indices = []
                    for coord in coordenadasPlanificadas:
                        indices.append(coordenadasDosComponentes.index(coord))

                    # print(indices)

                    componentesOrdenados = []

                    for indice in indices:
                        componentesOrdenados.append(componentesComMesh[indice])
                        print(componentesComMesh[indice])

                    # Calculo dos tempos da tarefa

                    tempoPorComponente = (tarefaCronograma.tempoFinalTarefa - \
                                          tarefaCronograma.tempoInicialDaTarefa) / len(componentesComMesh)
                    incremento = unreal.MathLibrary.round(
                        tempoPorComponente*sequenceFrameRate.numerator)
                    inicio = unreal.MathLibrary.round(
                        tarefaCronograma.tempoInicialDaTarefa*sequenceFrameRate.numerator)
                    fim = unreal.MathLibrary.round(
                        tarefaCronograma.tempoFinalTarefa*sequenceFrameRate.numerator)

                    if dividirComponentes:
                        frameInicial = unreal.FrameNumber(inicio)
                        frameFinal = unreal.FrameNumber(inicio + incremento)
                        frameAntesDoInicial = unreal.FrameNumber(inicio-1)
                        frameAposOFinal = unreal.FrameNumber(
                            inicio + incremento + 1)
                        print("Tempo inicial da tarefa: " + \
                              str(tarefaCronograma.tempoInicialDaTarefa))
                        print("Tempo final da tarefa: " + \
                              str(tarefaCronograma.tempoFinalTarefa))
                        print("Tempo por componente: " + \
                              str(tempoPorComponente))
                        print("Frame Incremento: " + str(incremento))
                        print("Frame inicial: " + str(frameInicial))
                        print("Frame final: " + str(frameFinal))
                        print("Frame anterior ao inicial: " + \
                              str(frameAntesDoInicial))
                        print("Frame após o final: " + str(frameAposOFinal))

                        for i in range(len(componentesOrdenados)):

                            if animacao == "Montagem":
                                print("Animação: Montagem")
                                component = componentesOrdenados[i]
                                componentBinding = levelSequence.add_possessable(
                                    component)

                                CriarTrackVisibilidadeComponente(
                                    componentBinding, frameAntesDoInicial, frameInicial)

                                CriarTrackTrocaDeMaterial(
                                    componentBinding, component, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal)

                                CriarTrackMoverComponenteEmZ(
                                    selectedActors[0], component, componentBinding, frameInicial, frameFinal)

                            elif animacao == "PreencherZ":
                                print("Animação: PreencherZ")
                                component = componentesOrdenados[i]
                                componentBinding = levelSequence.add_possessable(
                                    component)

                                CriarTrackVisibilidadeComponente(
                                    componentBinding, frameAntesDoInicial, frameInicial)

                                CriarTrackTrocaDeMaterial(
                                    componentBinding, component, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal)

                                CriarTrackParametroDeMaterial(
                                    componentBinding, frameInicial, frameFinal)

                            else:
                                component = componentesOrdenados[i]
                                componentBinding = levelSequence.add_possessable(
                                    component)

                                CriarTrackVisibilidadeComponente(
                                    componentBinding, frameAntesDoInicial, frameInicial)

                                CriarTrackTrocaDeMaterial(
                                    componentBinding, component, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal)

                                CriarTrackParametroDeMaterial(
                                    componentBinding, frameInicial, frameFinal)

                            frameAntesDoInicial = unreal.FrameNumber(
                                frameAntesDoInicial.value + incremento)
                            frameInicial = unreal.FrameNumber(
                                frameInicial.value + incremento)
                            frameFinal = unreal.FrameNumber(
                                frameFinal.value + incremento)
                            frameAposOFinal = unreal.FrameNumber(
                                frameAposOFinal.value + incremento)

                    else:

                        frameInicial = unreal.FrameNumber(inicio)
                        frameFinal = unreal.FrameNumber(fim)
                        frameAntesDoInicial = unreal.FrameNumber(inicio-1)
                        frameAposOFinal = unreal.FrameNumber(fim + 1)

                        print(frameInicial)
                        print(frameFinal)
                        print(animacao)

                        for i in range(len(componentesOrdenados)):

                            if animacao == "Montagem":
                                print("Animação: Montagem")
                                component = componentesOrdenados[i]
                                componentBinding = levelSequence.add_possessable(
                                    component)

                                CriarTrackVisibilidadeComponente(
                                    componentBinding, frameAntesDoInicial, frameInicial)

                                CriarTrackTrocaDeMaterial(
                                    componentBinding, component, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal)

                                CriarTrackMoverElementoEmZ(
                                    actor, componentBinding, frameInicial, frameFinal)

                            elif animacao == "PreencherZ":
                                print("Animação: PreencherZ")
                                component = componentesOrdenados[i]
                                componentBinding = levelSequence.add_possessable(
                                    component)

                                CriarTrackVisibilidadeComponente(
                                    componentBinding, frameAntesDoInicial, frameInicial)

                                CriarTrackTrocaDeMaterial(
                                    componentBinding, component, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal)

                                CriarTrackParametroDeMaterial(
                                    componentBinding, frameInicial, frameFinal)

                            elif animacao == "Simples":
                                print("Animação: Simples")
                                component = componentesOrdenados[i]
                                componentBinding = levelSequence.add_possessable(
                                    component)

                                CriarTrackVisibilidadeComponente(
                                    componentBinding, frameAntesDoInicial, frameInicial)

                                CriarTrackTrocaDeMaterial(
                                    componentBinding, component, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal)

                                CriarTrackParametroDeMaterial(
                                    componentBinding, frameInicial, frameFinal)


# region CÓDIGO ANTIGO

""" 
def CriarLevelSequenceComplexTracksB(dataTable, dataInicial, dataFinal, usedate, usefirstlastdate,
                                    coordenada_inicial="x", inverter_coordenada_inicial=False, coordenada_secundaria="y",
                                     inverter_coordenada_secundaria=False, tolerancia=100):

    # Calcular as datas do cronograma
    datas = CalcularDataInicialEFinal(
        dataTable, dataInicial, dataFinal, usedate, usefirstlastdate)

    dataInicial = datas[0]
    dataFinal = datas[1]

    # Pega a LevelSequence que esta aberta
    levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

    # Calcula o tempo base da sequence
    tempoTotalSequence = levelSequence.get_playback_end_seconds()
    diasTotais = CalcularDiasTotais(dataInicial, dataFinal)
    print('Dias totais: ' + str(diasTotais))
    sequenceFrameRate = levelSequence.get_display_rate()

    # Pega as colunas da DataTable
    dataTableColumns = PegarDadosDataTableCronograma(dataTable)

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Pega o LevelSequenceEditorSubSystem
    editorSubsystem = unreal.get_editor_subsystem(
        unreal.LevelSequenceEditorSubsystem)

    # Caso tenham colunas
    if len(dataTableColumns) > 0:

        # Para cada coluna
        for i in range(len(dataTableColumns[0])):

            tarefa = prefixTarefa + str(dataTableColumns[0][i])  # Nome da tarefa
            dataInicialTarefa = unreal.MathLibrary.date_time_from_string(
                dataTableColumns[1][i])
            dataFinalTarefa = unreal.MathLibrary.date_time_from_string(
                dataTableColumns[2][i])
            animacao = dataTableColumns[4][i]
            materialEfeito = unreal.load_object(name= dataTableColumns[3][i], outer = None)
            tempoInicialDaTarefa = CalcularTempoInicialDaTarefa(
                tempoTotalSequence, diasTotais, dataInicial, dataInicialTarefa)
            tempoFinalTarefa = CalcularTempoFinalDaTarefa(
                tempoTotalSequence, diasTotais, dataInicial, dataFinalTarefa)

            # Para cada ator selecionado
            for actor in selectedActors:

                if unreal.Array.count(actor.tags, unreal.Name.cast(tarefa)) > 0:  # Caso tenha uma tarefa da dataTable

                    # Adiciona o primeiro componente do ator como uma track
                    actorComponents = selectedActors[0].get_components_by_class(
                        unreal.StaticMeshComponent)

                    # Material Efeito
                    materialEfeito = unreal.load_object(name= '/Game/Materials/MS_SimpleGlow_Inst', outer = None)

                    # Filtra os componentes pegando apenas aqueles que possuem mesh
                    componentesComMesh = []

                    for component in actorComponents:
                        component = unreal.StaticMeshComponent.cast(component)
                        if unreal.SystemLibrary.is_valid(component.static_mesh):
                            componentesComMesh.append(component)

                    # Organiza os componentes de acordo com a posição

                    # Determina qual índice é correspondente a coordenada escolhida
                    coordenadaInicial = {"x": 0, "y": 1, "z": 2}[
                        coordenada_inicial]
                    coordenadaSecundaria = {"x": 0, "y": 1, "z": 2}[
                        coordenada_secundaria]
                    inverterCoordenadaInicial = inverter_coordenada_inicial
                    inverterCoordenadaSecundaria = inverter_coordenada_secundaria

                    print('QUANTIDADE DE COMPONENTES COM MESH:')
                    print(len(componentesComMesh))

                    coordenadasDosComponentes = PegarLocalizacaoDosComponentes(
                        componentesComMesh)

                    # print('COORDENADAS DOS COMPONENTES:')
                    # print(coordenadasDosComponentes)

                    coordenadasOrdenadas = AgruparEOrdenarPontosEmDuasCoordenadasComTolerancia(
                        coordenadasDosComponentes,
                        tolerancia,
                        tolerancia,
                        coordenadaInicial,
                        coordenadaSecundaria,
                        inverterCoordenadaInicial,
                        inverterCoordenadaSecundaria)

                    # print('COORDENADAS ORDENADAS:')
                    # print(coordenadasOrdenadas)

                    coordenadasPlanificadas = PlanificarListaDePontos(
                        coordenadasOrdenadas)

                    # print('COORDENADAS ORDENADAS PLANIFICADAS:')
                    # print(coordenadasPlanificadas)

                    indices = []
                    for coord in coordenadasPlanificadas:
                        indices.append(coordenadasDosComponentes.index(coord))

                    # print(indices)

                    componentesOrdenados = []

                    for indice in indices:
                        componentesOrdenados.append(componentesComMesh[indice])

                    # Calculo dos tempos da tarefa
                    tempoPorComponente = (
                        tempoFinalTarefa - tempoInicialDaTarefa) / len(componentesComMesh)
                    incremento = unreal.MathLibrary.round(
                        tempoPorComponente*sequenceFrameRate.numerator)
                    inicio = unreal.MathLibrary.round(
                        tempoInicialDaTarefa*sequenceFrameRate.numerator)
                    fim = unreal.MathLibrary.round(
                        tempoFinalTarefa*sequenceFrameRate.numerator)
                    frameInicial = unreal.FrameNumber(inicio)
                    frameFinal = unreal.FrameNumber(inicio + incremento)
                    frameAntesDoInicial = unreal.FrameNumber(inicio-1)
                    frameAposOFinal = unreal.FrameNumber(
                        inicio + incremento + 1)
                    print("Tempo inicial da tarefa: " + \
                          str(tempoInicialDaTarefa))
                    print("Tempo final da tarefa: " + str(tempoFinalTarefa))
                    print("Tempo por componente: " + str(tempoPorComponente))
                    print("Frame Incremento: " + str(incremento))
                    print("Frame inicial: " + str(frameInicial))
                    print("Frame final: " + str(frameFinal))
                    print("Frame anterior ao inicial: " + \
                          str(frameAntesDoInicial))
                    print("Frame após o final: " + str(frameAposOFinal))

                    for i in range(len(componentesOrdenados)):

                        print(frameInicial.value)

                        if animacao == "Montagem":
                            print("Animação: Montagem")
                            component = componentesOrdenados[i]
                            componentBinding = levelSequence.add_possessable(
                                component)

                            CriarTrackVisibilidadeComponente(
                                componentBinding, frameAntesDoInicial, frameInicial)

                            CriarTrackTrocaDeMaterial(
                                componentBinding, component, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal)

                            CriarTrackMoverComponenteEmZ(
                                selectedActors[0], component, componentBinding, frameInicial, frameFinal)

                        elif animacao == "PreencherZ":
                            print("Animação: PreencherZ")
                            component = componentesOrdenados[i]
                            componentBinding = levelSequence.add_possessable(
                                component)

                            CriarTrackVisibilidadeComponente(
                                componentBinding, frameAntesDoInicial, frameInicial)

                            CriarTrackTrocaDeMaterial(
                                componentBinding, component, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal)

                            CriarTrackParametroDeMaterial(
                                componentBinding, frameInicial, frameFinal)

                        frameAntesDoInicial = unreal.FrameNumber(
                            frameAntesDoInicial.value + incremento)
                        frameInicial = unreal.FrameNumber(
                            frameInicial.value + incremento)
                        frameFinal = unreal.FrameNumber(
                            frameFinal.value + incremento)
                        frameAposOFinal = unreal.FrameNumber(
                            frameAposOFinal.value + incremento)


def CriarLevelSequenceComplexTracksBB(coordenada_inicial="x", inverter_coordenada_inicial=False, coordenada_secundaria="y", inverter_coordenada_secundaria=False):

    # Pega a LevelSequence que esta aberta
    levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Pega o LevelSequenceEditorSubSystem
    editorSubsystem = unreal.get_editor_subsystem(
        unreal.LevelSequenceEditorSubsystem)

    # Adiciona o primeiro componente do ator como uma track
    actorComponents = selectedActors[0].get_components_by_class(
        unreal.StaticMeshComponent)

    # Material Efeito
    materialEfeito = unreal.load_object(name= '/Game/Materials/MS_SimpleGlow_Inst', outer = None)

    # Filtra os componentes pegando apenas aqueles que possuem mesh
    componentesComMesh = []

    for component in actorComponents:
        component = unreal.StaticMeshComponent.cast(component)
        if unreal.SystemLibrary.is_valid(component.static_mesh):
            componentesComMesh.append(component)

    # Organiza os componentes de acordo com a posição

    # Determina qual índice é correspondente a coordenada escolhida
    coordenadaInicial = {"x": 0, "y": 1, "z": 2}[coordenada_inicial]
    coordenadaSecundaria = {"x": 0, "y": 1, "z": 2}[coordenada_secundaria]
    inverterCoordenadaInicial = inverter_coordenada_inicial
    inverterCoordenadaSecundaria = inverter_coordenada_secundaria
    tolerancia = 100

    print('QUANTIDADE DE COMPONENTES COM MESH:')
    print(len(componentesComMesh))

    coordenadasDosComponentes = PegarLocalizacaoDosComponentes(
        componentesComMesh)

    print('COORDENADAS DOS COMPONENTES:')
    print(coordenadasDosComponentes)

    coordenadasOrdenadas = AgruparEOrdenarPontosEmDuasCoordenadasComTolerancia(
        coordenadasDosComponentes,
        tolerancia,
        tolerancia,
        coordenadaInicial,
        coordenadaSecundaria,
        inverterCoordenadaInicial,
        inverterCoordenadaSecundaria)

    print('COORDENADAS ORDENADAS:')
    print(coordenadasOrdenadas)

    coordenadasPlanificadas = PlanificarListaDePontos(coordenadasOrdenadas)

    print('COORDENADAS ORDENADAS PLANIFICADAS:')
    print(coordenadasPlanificadas)

    indices = []
    for coord in coordenadasPlanificadas:
        indices.append(coordenadasDosComponentes.index(coord))

    print(indices)

    componentesOrdenados = []

    for indice in indices:
        componentesOrdenados.append(componentesComMesh[indice])

    # frames
    frameAntesDoInicial = unreal.FrameNumber(0)
    frameInicial = unreal.FrameNumber(1)
    frameFinal = unreal.FrameNumber(10)
    frameAposOFinal = unreal.FrameNumber(11)

    print(componentesComMesh[0].relative_location)
    print(componentesOrdenados[0].relative_location)

    for i in range(len(componentesOrdenados)):

        component = componentesOrdenados[i]
        componentBinding = levelSequence.add_possessable(component)

        CriarTrackVisibilidadeComponente(
            componentBinding, frameAntesDoInicial, frameInicial)

        CriarTrackTrocaDeMaterial(componentBinding, component, materialEfeito,
                                  frameAntesDoInicial, frameFinal, frameAposOFinal)

        CriarTrackMoverComponenteEmZ(
            selectedActors[0], component, componentBinding, frameInicial, frameFinal)

        frameAntesDoInicial = frameAntesDoInicial + unreal.FrameNumber(10)
        frameInicial = frameInicial + unreal.FrameNumber(10)
        frameFinal = frameFinal + unreal.FrameNumber(10)
        frameAposOFinal = frameAposOFinal + unreal.FrameNumber(10)


def CriarLevelSequenceTracksB(dataTable):

    print('CriarLevelSequenceTracks')

    # Pega os nomes das linhas da DataTable
    dtRowNames = dataTableLibrary.get_data_table_row_names(dataTable)

    # Para cada nome de linha criar uma track na sequence
    for rowName in dtRowNames:
        print(rowName)

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Verifica se o elemento selecionado é uma sequence
    if selectedActors[0].__class__ == unreal.LevelSequenceActor:

        # Cast o primeiro ator selecionado como LevelSequenceActor
        lsActor = unreal.LevelSequenceActor.cast(selectedActors[0])

        # Pega a LevelSequence que esta aberta
        levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

        # Pega todos os atores com a tag
        actorsWithTag = unreal.GameplayStatics.get_all_actors_of_class_with_tag(
            lsActor, unreal.StaticMeshActor, 'AYTF_FundacaoProfunda')
        print('Existem ' + str(len(actorsWithTag)) + ' Atores com a TAG')

        # Cria um Array com o primeiro ator
        firstActorArray = [actorsWithTag[0]]

        # Pega o LevelSequenceEditorSubSystem
        editorSubsystem = unreal.get_editor_subsystem(
            unreal.LevelSequenceEditorSubsystem)

        bindings = unreal.MovieSceneSequence.get_bindings(levelSequence)

        for bind in bindings:
            tracks = bind.get_tracks()
            for track in tracks:
                print(track)
                sections = track.get_sections()
                for section in sections:
                    print(section)
                    channelsParameter = section.get_all_channels()
                    for channel in channelsParameter:
                        print(channel)

        # Adiciona o primeiro ator a Sequence
        # actorTrack = editorSubsystem.add_actors(firstActorArray)

        # Adiciona o primeiro componente do ator como uma track
        actorComponent = firstActorArray[0].get_component_by_class(
            unreal.StaticMeshComponent)
        componentBinding = levelSequence.add_possessable(actorComponent)

        # Adiciona uma track para alterar o valor do material do component
        materialValueTrack = componentBinding.add_track(
            unreal.MovieSceneComponentMaterialTrack)

        # Adiciona uma track para alterar o material do component
        materialChangeTrack = componentBinding.add_track(
            unreal.MovieScenePrimitiveMaterialTrack)

        # Adiciona uma track para alterar a visibilidade do ator
        visibilityTrack = componentBinding.get_parent(
        ).add_track(unreal.MovieSceneVisibilityTrack)

        # Adiciona uma seção com propriedade as tracks
        newSectionValue = materialValueTrack.add_section()
        newSectionMaterial = materialChangeTrack.add_section()
        newSectionVisibility = visibilityTrack.add_section()

        # Cast as seçãos criadas para seus tipos corretos
        parameterSection = unreal.MovieSceneParameterSection.cast(
            newSectionValue)
        materialChangeSection = unreal.MovieScenePrimitiveMaterialSection.cast(
            newSectionMaterial)
        visibilitySection = unreal.MovieSceneBoolSection.cast(
            newSectionVisibility)

        # Refresh na Sequence para mostrar as alterações
        unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

        # Adiciona uma chave de parâmetro escalar e define seu valor
        inicio = 100
        fim = 200
        inicioFrame = unreal.FrameNumber(inicio)
        fimFrame = unreal.FrameNumber(fim)
        antesDoInicioFrame = unreal.FrameNumber(inicio-1)
        aposOFimFrame = unreal.FrameNumber(fim+1)

        # Adiciona uma chave para criar automaticamente um channel e poder adicionar as chaves corretamente depois
        parameterSection.add_scalar_parameter_key(
            "Curve", unreal.FrameNumber(0), 0.0)

        # Pega todos os channels da seção
        channelsParameter = parameterSection.get_all_channels()
        channelsMaterial = materialChangeSection.get_all_channels()
        channelsVisibility = visibilitySection.get_all_channels()

        # Cast o channel
        floatChannel = unreal.MovieSceneScriptingFloatChannel.cast(
            channelsParameter[0])
        materialChannel = unreal.MovieSceneScriptingObjectPathChannel.cast(
            channelsMaterial[0])
        boolChannel = unreal.MovieSceneScriptingBoolChannel.cast(
            channelsVisibility[0])

        # Pega os materiais
        materialObjeto = unreal.load_object(name= '/Game/Materials/M_CorBranca', outer = None)
        print(materialObjeto)
        materialEfeito = unreal.load_object(name= '/Game/Materials/MS_SimpleGlow_Inst', outer = None)
        print(materialEfeito)

        # Adiciona as chaves corretamente
        floatChannel.add_key(inicioFrame, 0.0, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        floatChannel.add_key(fimFrame, 2.0, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)

        # materialChannel.add_key(antesDoInicioFrame,materialObjeto,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        materialChannel.add_key(antesDoInicioFrame, materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        materialChannel.add_key(fimFrame, materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        materialChannel.add_key(aposOFimFrame, materialObjeto,0,unreal.SequenceTimeUnit.DISPLAY_RATE)

        boolChannel.add_key(antesDoInicioFrame, False, 0,
                            unreal.SequenceTimeUnit.DISPLAY_RATE)
        boolChannel.add_key(inicioFrame, True, 0,
                            unreal.SequenceTimeUnit.DISPLAY_RATE)

        # Remove a chave padrão
        chavePadrao = floatChannel.get_keys()[0]
        floatChannel.remove_key(chavePadrao)

        # Define o range da seção
        newSectionValue.set_start_frame_bounded(True)
        newSectionValue.set_end_frame_bounded(True)

        # Adiciona todos os atores com a mesma TAG a track
        editorSubsystem.add_actors_to_binding(
            actorsWithTag, componentBinding.get_parent())


        # unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

        # newSection.add
        # floatTrack = componentBinding.add_track(unreal.MovieSceneMaterialParameterSection)

        # componentBinding.set_parent(actorsWithTag[0])

        # # Adiciona todos os atores com a mesma TAG a track
        # editorSubsystem.add_actors_to_binding(actorsWithTag, actorTrack[0])

        # # Adiciona uma track para alterar o material do component
        # materialTrack = actorTrack[0].add_track(unreal.MovieSceneComponentMaterialTrack)

        # # Adiciona uma seção a track de material
        #
        # newSection.
        # section.set_compo

        # Define o componente da seção

        # # Define o range da seção
        # newSection.set_range(100,200)

        # # Pega os canais da seção
        # channels = newSection.get_channels()

        # # # Adiciona um novo canal a seção
        # channels.

        #
        # channel = newSection.get_channels()[0]


        # bindings = unreal.MovieSceneSequence.get_bindings(levelSequence)

        # print('Quantidade de BINDINGS: ' + str(len(bindings)))

        # trackPadraomaterial = []

        # # Duplica a track
        # for bind in bindings:
        #     if bind.get_display_name() == 'TrackMaterialPadrao':
        #         print('Encontrou a track TrackMaterialPadrao')
        #         trackPadraomaterial.append(bind)
        #     # for track in tracks:
        #     #     print(track)
        #         # if track.get_display_name() == 'TrackMaterialPadrao':
        #         #     trackPadraomaterial.append(track)
        #         #     print('Encontrou a track TrackMaterialPadrao')
        #         #     sections = track.get_sections()

        # actorTrack = print(levelSequenceSubSystem)

        # for actor in actorsWithTag:

        #     copiedTrack = unreal.LevelSequenceEditorSubsystem.copy_tracks(trackPadraomaterial)
        #     print(copiedTrack)

        # for bind in bindings:
        #     tracks = bind.get_tracks()
        #     for track in tracks:
        #         print(track.get_display_name())
        #         sections = track.get_sections()
        #         for section in sections:
        #             print(section)
        #             channels = section.get_all_channels()
        #             for channel in channels:
        #                 print(channel)

        # # Adiciona uma track com binding para os atores
        # firstBind = levelSequence.add_possessable(actorsWithTag[0])
        # materialTrack = firstBind.add_track(unreal.MovieSceneComponentMaterialTrack)
        # newSection = materialTrack.add_section()
        # newSection.set_range(100,200)
        # channel = newSection.get_channels()[0]
        # channel.add
        # unreal.MovieSceneScriptingFloatChannel.add_key(channel, 10,0,0,unreal.SequenceTimeUnit.DISPLAY_RATE, unreal.MovieSceneKeyInterpolation.AUTO)
        # #MovieSceneScriptingFloatChannel


        # for bind in bindings:
        #     tracks = bind.get_tracks()
        #     for track in tracks:
        #         print(track)
        #         sections = track.get_sections()
        #         for section in sections:
        #             print(section)
        #             channels = section.get_all_channels()
        #             for channel in channels:
        #                 print(channel)


           # print(bind)


        # Pega as MasterTracks da sequence e limpa as mesmas

        # masterTracks = unreal.MovieSceneSequence.get_master_tracks(movieSequence)
        # bindings = unreal.MovieSceneSequence.get_bindings(movieSequence)
        # masterTracksnames = []

        # for bind in bindings:
        #     print(bind.get_display_name())

        # for masterTrack in masterTracks:
        #     # unreal.MovieSceneSequence.remove_master_track(movieSequence, masterTrack)
        #     trackName = masterTrack.get_display_name()
        #     print(trackName)
        #     # masterTracksnames.append(trackName)

        # Pega os nomes das linhas da DataTable
        # dtRowNames = dataTableLibrary.get_data_table_row_names(dataTable)

        # Para cada nome de linha criar uma track na sequence
        # for rowName in dtRowNames:
        #     newTrack = movieSequence.add_master_track(unreal.MovieSc)
        #     unreal.MovieSceneTrackExtensions.set_display_name(newTrack, rowName) # Define o nome da track


        # any(s for s in actorTagsString if s.startswith(prefixo)):


        #    print(rowName)
        #     print(unreal.DataTableRowHandle(dataTable, rowName))

    else:
        print('Não é um LevelSequenceActor, selecione um LevelSequenceActor no Level')


def CriarLevelSequenceTracksBB(dataTable, dataInicial, dataFinal, usedate, usefirstlastdate):

    dataInicial = dataInicial
    dataFinal = dataFinal

    if usedate:

        # Calcula as datas iniciais e finais do cronograma
        dataInicial, dataFinal = CalcularDatasIniciaisEFinais(
            dataTable, usefirstlastdate)

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))
    elif usefirstlastdate:

        # Calcula as datas iniciais e finais do cronograma
        dataInicial, dataFinal = CalcularDatasIniciaisEFinais(
            dataTable, usefirstlastdate)

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))
    else:
        # Converte as datas de string dd/mm/yyyy para DataTimeStructure da Unreal
        arrDataInicial = unreal.StringLibrary.parse_into_array(dataInicial, "/",False)
        arrDataFinal = unreal.StringLibrary.parse_into_array(dataFinal, "/",False)

        dataInicial = "{0}-{1}-{2}-12.00.00".format(
            arrDataInicial[2], arrDataInicial[1], arrDataInicial[0])
        dataFinal = "{0}-{1}-{2}-12.00.00".format(
            arrDataFinal[2], arrDataFinal[1], arrDataFinal[0])

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))

        dataInicial = unreal.MathLibrary.date_time_from_string(dataInicial)
        dataFinal = unreal.MathLibrary.date_time_from_string(dataFinal)

    # Pega a LevelSequence que esta aberta
    levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Calcula o tempo base da sequence
    tempoTotalSequence = levelSequence.get_playback_end_seconds()
    diasTotais = CalcularDiasTotais(dataInicial, dataFinal)
    print('Dias totais: ' + str(diasTotais))
    sequenceFrameRate = levelSequence.get_display_rate()

    # Pega o LevelSequenceEditorSubSystem
    editorSubsystem = unreal.get_editor_subsystem(
        unreal.LevelSequenceEditorSubsystem)

    # Pega as colunas da DataTable
    dataTableColumns = PegarDadosDataTableCronograma(dataTable)

    # Caso tenham colunas
    if len(dataTableColumns) > 0:
        # Para cada coluna
        for i in range(len(dataTableColumns[0])):

            tarefa = prefixTarefa + str(dataTableColumns[0][i])  # Nome da tarefa
            dataInicialTarefa = unreal.MathLibrary.date_time_from_string(
                dataTableColumns[1][i])
            dataFinalTarefa = unreal.MathLibrary.date_time_from_string(
                dataTableColumns[2][i])
            animacao = dataTableColumns[4][i]
            materialEfeito = unreal.load_object(name= dataTableColumns[3][i], outer = None)

            tempoInicialDaTarefa = CalcularTempoInicialDaTarefa(
                tempoTotalSequence, diasTotais, dataInicial, dataInicialTarefa)
            tempoFinalTarefa = CalcularTempoFinalDaTarefa(
                tempoTotalSequence, diasTotais, dataInicial, dataFinalTarefa)

            # Pega todos os atores com a tag
            actorsWithTag = unreal.GameplayStatics.get_all_actors_of_class_with_tag(
                selectedActors[0], unreal.StaticMeshActor, tarefa)

            # Filtra para apenas os selecionados
            actorsSelecionados = []
            for actor in actorsWithTag:
                if actor in selectedActors:
                    actorsSelecionados.append(actor)

            actorsWithTag = actorsSelecionados
            # print('Existem ' + str(len(actorsWithTag)) + ' Atores com a TAG ' + str(tarefa))

            # Cria um Array com o primeiro ator caso existam atores com a tag
            if len(actorsWithTag) > 0:

                # Cria um Array com o primeiro ator
                firstActorArray = [actorsWithTag[0]]

                # Calcula os tempos em FRAMES
                inicio = unreal.MathLibrary.round(
                    tempoInicialDaTarefa*sequenceFrameRate.numerator)
                fim = unreal.MathLibrary.round(
                    tempoFinalTarefa*sequenceFrameRate.numerator)
                frameInicial = unreal.FrameNumber(inicio)
                frameFinal = unreal.FrameNumber(fim)
                frameAntesDoInicial = unreal.FrameNumber(inicio-1)
                frameAposOFinal = unreal.FrameNumber(fim+1)

                # Pega o LevelSequenceEditorSubSystem
                editorSubsystem = unreal.get_editor_subsystem(
                    unreal.LevelSequenceEditorSubsystem)

                # Adiciona o primeiro ator a Sequence
                # actorTrack = editorSubsystem.add_actors(firstActorArray)

                # Adiciona o primeiro componente do ator como uma track
                actorComponent = firstActorArray[0].get_component_by_class(
                    unreal.StaticMeshComponent)
                componentBinding = levelSequence.add_possessable(
                    actorComponent)

                CriarTrackVisibilidade(
                    componentBinding, frameAntesDoInicial, frameInicial)

                CriarTrackTrocaDeMaterial(componentBinding, actorComponent, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal)

                CriarTrackParametroDeMaterial(
                    componentBinding, frameInicial, frameFinal)

                if animacao == "Montagem":
                    CriarTrackMoverElementoEmZ(
                        actor, componentBinding, frameInicial, frameFinal)

                # Adiciona todos os atores com a mesma TAG a track
                editorSubsystem.add_actors_to_binding(
                    actorsWithTag, componentBinding.get_parent())

                # Renomeia a track
                componentBinding.get_parent().set_display_name(
                    str(dataTableColumns[0][i]))
    else:
        print('Nenhum dado encontrado na DataTable')


def CriarLevelSequenceTracksBB(dataTable, dataInicial, dataFinal, usedate, usefirstlastdate):

    dataInicial = dataInicial
    dataFinal = dataFinal

    if usedate:

        # Calcula as datas iniciais e finais do cronograma
        dataInicial, dataFinal = CalcularDatasIniciaisEFinais(
            dataTable, usefirstlastdate)

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))
    elif usefirstlastdate:

        # Calcula as datas iniciais e finais do cronograma
        dataInicial, dataFinal = CalcularDatasIniciaisEFinais(
            dataTable, usefirstlastdate)

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))
    else:
        # Converte as datas de string dd/mm/yyyy para DataTimeStructure da Unreal
        arrDataInicial = unreal.StringLibrary.parse_into_array(dataInicial, "/",False)
        arrDataFinal = unreal.StringLibrary.parse_into_array(dataFinal, "/",False)

        dataInicial = "{0}-{1}-{2}-12.00.00".format(
            arrDataInicial[2], arrDataInicial[1], arrDataInicial[0])
        dataFinal = "{0}-{1}-{2}-12.00.00".format(
            arrDataFinal[2], arrDataFinal[1], arrDataFinal[0])

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))

        dataInicial = unreal.MathLibrary.date_time_from_string(dataInicial)
        dataFinal = unreal.MathLibrary.date_time_from_string(dataFinal)

    # Pega a LevelSequence que esta aberta
    levelSequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

    # Pega os atores selectionados
    actorSubSystem = unreal.get_editor_subsystem(actorUtils)
    selectedActors = actorSubSystem.get_selected_level_actors()

    # Calcula o tempo base da sequence
    tempoTotalSequence = levelSequence.get_playback_end_seconds()
    diasTotais = CalcularDiasTotais(dataInicial, dataFinal)
    print('Dias totais: ' + str(diasTotais))
    sequenceFrameRate = levelSequence.get_display_rate()

    # Pega o LevelSequenceEditorSubSystem
    editorSubsystem = unreal.get_editor_subsystem(
        unreal.LevelSequenceEditorSubsystem)

    # Pega as colunas da DataTable
    dataTableColumns = PegarDadosDataTableCronograma(dataTable)

    # Caso tenham colunas
    if len(dataTableColumns) > 0:
        # Para cada coluna
        for i in range(len(dataTableColumns[0])):

            tarefa = prefixTarefa + str(dataTableColumns[0][i])  # Nome da tarefa
            dataInicialTarefa = unreal.MathLibrary.date_time_from_string(
                dataTableColumns[1][i])
            dataFinalTarefa = unreal.MathLibrary.date_time_from_string(
                dataTableColumns[2][i])
            animacao = dataTableColumns[3][i]

            tempoInicialDaTarefa = CalcularTempoInicialDaTarefa(
                tempoTotalSequence, diasTotais, dataInicial, dataInicialTarefa)
            tempoFinalTarefa = CalcularTempoFinalDaTarefa(
                tempoTotalSequence, diasTotais, dataInicial, dataFinalTarefa)

            # print('Tarefa: ' + tarefa + 'Tempo inicial: ' + str(tempoInicialDaTarefa) + 'Tempo final: ' + str(tempoFinalTarefa))

            # Pega todos os atores com a tag
            actorsWithTag = unreal.GameplayStatics.get_all_actors_of_class_with_tag(
                selectedActors[0], unreal.StaticMeshActor, tarefa)

            # Filtra para apenas os selecionados
            actorsSelecionados = []
            for actor in actorsWithTag:
                if actor in selectedActors:
                    actorsSelecionados.append(actor)

            actorsWithTag = actorsSelecionados
            # print('Existem ' + str(len(actorsWithTag)) + ' Atores com a TAG ' + str(tarefa))

            # Cria um Array com o primeiro ator caso existam atores com a tag
            if len(actorsWithTag) > 0:

                # Cria um Array com o primeiro ator
                firstActorArray = [actorsWithTag[0]]

                # Calcula os tempos em FRAMES
                inicio = unreal.MathLibrary.round(
                    tempoInicialDaTarefa*sequenceFrameRate.numerator)
                fim = unreal.MathLibrary.round(
                    tempoFinalTarefa*sequenceFrameRate.numerator)
                inicioFrame = unreal.FrameNumber(inicio)
                fimFrame = unreal.FrameNumber(fim)
                antesDoInicioFrame = unreal.FrameNumber(inicio-1)
                aposOFimFrame = unreal.FrameNumber(fim+1)

                # Pega o LevelSequenceEditorSubSystem
                editorSubsystem = unreal.get_editor_subsystem(
                    unreal.LevelSequenceEditorSubsystem)

                # Adiciona o primeiro ator a Sequence
                # actorTrack = editorSubsystem.add_actors(firstActorArray)

                # Adiciona o primeiro componente do ator como uma track
                actorComponent = firstActorArray[0].get_component_by_class(
                    unreal.StaticMeshComponent)
                componentBinding = levelSequence.add_possessable(
                    actorComponent)

                # Adiciona uma track para alterar o valor do material do component
                materialValueTrack = componentBinding.add_track(
                    unreal.MovieSceneComponentMaterialTrack)

                # Adiciona uma track para alterar o material do component
                materialChangeTrack = componentBinding.add_track(
                    unreal.MovieScenePrimitiveMaterialTrack)

                # Adiciona uma track para alterar a visibilidade do ator
                visibilityTrack = componentBinding.get_parent(
                ).add_track(unreal.MovieSceneVisibilityTrack)

                # Adiciona uma seção com propriedade as tracks
                newSectionValue = materialValueTrack.add_section()
                newSectionMaterial = materialChangeTrack.add_section()
                newSectionVisibility = visibilityTrack.add_section()

                # Cast as seçãos criadas para seus tipos corretos
                parameterSection = unreal.MovieSceneParameterSection.cast(
                    newSectionValue)
                materialChangeSection = unreal.MovieScenePrimitiveMaterialSection.cast(
                    newSectionMaterial)
                visibilitySection = unreal.MovieSceneBoolSection.cast(
                    newSectionVisibility)

                # Refresh na Sequence para mostrar as alterações
                unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

                # Adiciona uma chave para criar automaticamente um channel e poder adicionar as chaves corretamente depois
                parameterSection.add_scalar_parameter_key(
                    "Curve", unreal.FrameNumber(0), 0.0)

                # Pega todos os channels da seção
                channelsParameter = parameterSection.get_all_channels()
                channelsMaterial = materialChangeSection.get_all_channels()
                channelsVisibility = visibilitySection.get_all_channels()

                # Cast o channel
                floatChannel = unreal.MovieSceneScriptingFloatChannel.cast(
                    channelsParameter[0])
                materialChannel = unreal.MovieSceneScriptingObjectPathChannel.cast(
                    channelsMaterial[0])
                boolChannel = unreal.MovieSceneScriptingBoolChannel.cast(
                    channelsVisibility[0])

                # Pega os materiais
                # materialObjeto = unreal.load_object(name = '/Game/Materials/M_CorBranca', outer = None)
                materialObjeto = unreal.StaticMeshComponent.cast(
                    actorComponent).get_material(0)
                # materialEfeito = unreal.load_object(name = '/Game/Materials/MS_SimpleGlow_Inst', outer = None)
                materialEfeito = unreal.load_object(name= dataTableColumns[3][i], outer = None)

                # Adiciona as chaves corretamente
                floatChannel.add_key(inicioFrame, 0.0, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)
                floatChannel.add_key(fimFrame, 2.0, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)

                # materialChannel.add_key(antesDoInicioFrame,materialObjeto,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
                materialChannel.add_key(antesDoInicioFrame, materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
                materialChannel.add_key(fimFrame, materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
                materialChannel.add_key(aposOFimFrame, materialObjeto,0,unreal.SequenceTimeUnit.DISPLAY_RATE)

                boolChannel.add_key(antesDoInicioFrame, False,
                                    0, unreal.SequenceTimeUnit.DISPLAY_RATE)
                boolChannel.add_key(inicioFrame, True, 0,
                                    unreal.SequenceTimeUnit.DISPLAY_RATE)

                # Remove a chave padrão
                chavePadrao = floatChannel.get_keys()[0]
                floatChannel.remove_key(chavePadrao)

                # Define o range da seção
                newSectionValue.set_start_frame_bounded(True)
                newSectionValue.set_end_frame_bounded(True)

                # Adiciona todos os atores com a mesma TAG a track
                editorSubsystem.add_actors_to_binding(
                    actorsWithTag, componentBinding.get_parent())

                # Renomeia a track
                componentBinding.get_parent().set_display_name(
                    str(dataTableColumns[0][i]))
    else:
        print('Nenhum dado encontrado na DataTable')

 """

# endregion

# endregion

# region SUBFUNÇÕES


def CalcularDatasIniciaisEFinais(dataTable, usarMesCompleto):

    # Pega as colunas da DataTable
    dataTableColumns = PegarDadosDataTableCronograma(dataTable)

    datasIniciais = []
    datasFinais = []

    for i in range(len(dataTableColumns[0])):
        datasIniciais.append(
            unreal.MathLibrary.date_time_from_string(dataTableColumns[1][i]))
        datasFinais.append(
            unreal.MathLibrary.date_time_from_string(dataTableColumns[2][i]))

    dataInicial = datasIniciais[0]
    dataFinal = datasFinais[0]

    for data in datasIniciais:
        if unreal.MathLibrary.less_date_time_date_time(data, dataInicial):
            dataInicial = data

    for data in datasFinais:
        if unreal.MathLibrary.greater_date_time_date_time(data, dataFinal):
            dataFinal = data

    # Caso usarMesCompleto então usar o primeiro e ultimo dia dos meses inicial e final
    if usarMesCompleto:
        mesInicial = unreal.MathLibrary.get_month(dataInicial)
        anoInicial = unreal.MathLibrary.get_year(dataInicial)

        mesFinal = unreal.MathLibrary.get_month(dataFinal)
        anoFinal = unreal.MathLibrary.get_year(dataFinal)
        diasDomesFinal = unreal.MathLibrary.days_in_month(anoFinal, mesFinal)

        stringDataInicial = "{0}-{1}-{2}-12.00.00".format(
            anoInicial, mesInicial, 1)
        stringDataFinal = "{0}-{1}-{2}-12.00.00".format(
            anoFinal, mesFinal, diasDomesFinal)
        dataInicial = unreal.MathLibrary.date_time_from_string(
            stringDataInicial)
        dataFinal = unreal.MathLibrary.date_time_from_string(stringDataFinal)

    return dataInicial, dataFinal


def AdicionarTagPorMetadata(chave, prefixo):

    actorsValores = dataSmithLibrary.get_all_objects_and_values_for_key(
        chave, unreal.Actor)

    if len(actorsValores[0]) > 0:

        actors = actorsValores[0]
        valores = actorsValores[1]

        # Para cada ator com a tarefa pegar suas tags e alterar o valor
        for i in range(len(actors)):
            actor = actors[i]
            actorTags = actor.tags
            actorTagsString = []
            for tag in actorTags:
                actorTagsString.append(str(tag))

            if any(s for s in actorTagsString if s.startswith(prefixo)):
                tagIndex = actorTagsString.index(
                    [s for s in actorTagsString if s.startswith(prefixo)][0])
                actorTags[tagIndex] = (prefixo + valores[i])
            else:
                actorTags.append(prefixo + valores[i])


def CriarTag(prefixo, tag, tagStrings, tags):
    if tag is not None:
        if any(s for s in tagStrings if s.startswith(prefixo)):
            index = tagStrings.index(
                [s for s in tagStrings if s.startswith(prefixo)][0])
            tags[index] = (prefixo + tag)
        else:
            tags.append(prefixo + tag)


def DeletarTag(prefixo, tagStrings, tags):
    if any(s for s in tagStrings if s.startswith(prefixo)):
        index = tagStrings.index(
            [s for s in tagStrings if s.startswith(prefixo)][0])
        unreal.Array.pop(tags, index)


def PegarDadosDataTableCronograma(dataTable):

    print('PegarDadosDataTableCronograma')

    # Estrutura da DataTable
    # structure = unreal.load_object(name = '/Game/Timeline/STR_CronogramaStruct.STR_CronogramaStruct', outer = None)

    # Pega os nomes das linhas da DataTable
    dtRowNames = unreal.DataTableFunctionLibrary.get_data_table_row_names(
        dataTable)

    # Colunas da DataTable
    dataTableColumns = []
    columnInicio = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(
        dataTable, 'Inicio')
    columnTermino = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(
        dataTable, 'Termino')
    columnMaterialEfeito = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(
        dataTable, 'MaterialEfeito')
    columnAnimacao = unreal.DataTableFunctionLibrary.get_data_table_column_as_string(
        dataTable, 'Animacao')

    dataTableColumns.append(dtRowNames)
    dataTableColumns.append(columnInicio)
    dataTableColumns.append(columnTermino)
    dataTableColumns.append(columnMaterialEfeito)
    dataTableColumns.append(columnAnimacao)

    return dataTableColumns


def CalcularDataInicialEFinal(dataTable, dataInicial, dataFinal, usedate, usefirstlastdate):

    dataInicial = dataInicial
    dataFinal = dataFinal

    if usedate:

        # Calcula as datas iniciais e finais do cronograma
        dataInicial, dataFinal = CalcularDatasIniciaisEFinais(
            dataTable, usefirstlastdate)

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))
    elif usefirstlastdate:

        # Calcula as datas iniciais e finais do cronograma
        dataInicial, dataFinal = CalcularDatasIniciaisEFinais(
            dataTable, usefirstlastdate)

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))
    else:
        # Converte as datas de string dd/mm/yyyy para DataTimeStructure da Unreal
        arrDataInicial = unreal.StringLibrary.parse_into_array(dataInicial, "/",False)
        arrDataFinal = unreal.StringLibrary.parse_into_array(dataFinal, "/",False)

        dataInicial = "{0}-{1}-{2}-12.00.00".format(
            arrDataInicial[2], arrDataInicial[1], arrDataInicial[0])
        dataFinal = "{0}-{1}-{2}-12.00.00".format(
            arrDataFinal[2], arrDataFinal[1], arrDataFinal[0])

        print("Data inicial: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataInicial)))
        print("Data final: " + unreal.TextLibrary.conv_text_to_string(
            unreal.TextLibrary.as_date_date_time(dataFinal)))

        dataInicial = unreal.MathLibrary.date_time_from_string(dataInicial)
        dataFinal = unreal.MathLibrary.date_time_from_string(dataFinal)

    return dataInicial, dataFinal


def CalcularDiasTotais(dataInicial, dataFinal):

    dataInicial = unreal.DateTime.cast(dataInicial)
    dataFinal = unreal.DateTime.cast(dataFinal)

    diasTotais = unreal.MathLibrary.get_days(
        unreal.MathLibrary.subtract_date_time_date_time(dataFinal, dataInicial))

    return (diasTotais)


def CalcularTempoInicialDaTarefa(tempoDaSequence, diasTotais, dataInicial, dataInicialTarefa):

    dataInicial = unreal.DateTime.cast(dataInicial)
    dataInicialTarefa = unreal.DateTime.cast(dataInicialTarefa)

    diasAteIniciarATarefa = unreal.MathLibrary.get_days(
        unreal.MathLibrary.subtract_date_time_date_time(dataInicialTarefa, dataInicial))

    # print(diasAteIniciarATarefa)

    tempoInicial = (diasAteIniciarATarefa / diasTotais) * tempoDaSequence

    return tempoInicial


def CalcularTempoFinalDaTarefa(tempoDaSequence, diasTotais, dataInicial, dataFinalTarefa):

    dataInicial = unreal.DateTime.cast(dataInicial)
    dataFinalTarefa = unreal.DateTime.cast(dataFinalTarefa)

    diasAteFinalizarATarefa = unreal.MathLibrary.get_days(
        unreal.MathLibrary.subtract_date_time_date_time(dataFinalTarefa, dataInicial))

    # print(diasAteFinalizarATarefa)

    tempoFinal = (diasAteFinalizarATarefa / diasTotais) * tempoDaSequence

    return tempoFinal

def AgruparEOrdenarPontosEmDuasCoordenadasComTolerancia(pontos, toleranciaA, toleranciaB, coordenadaA=0, coordenadaB=1, inverterA=False, inverterB=False):
    print('AgruparEOrdenarPontosEmDuasCoordenadasComTolerancia')
    gruposDePontos = AgruparPontosComTolerancia(
        pontos, toleranciaA, coordenadaA, inverterA)

    gruposOrdenados = []

    for grupo in gruposDePontos:
        gruposOrdenados.append(OrdenarPontos(grupo, coordenadaB, inverterB))

    return gruposOrdenados


def AgruparPontosComTolerancia(pontos, tolerancia, coordenada=0, inverter=False):
    print("AgruparPontosComTolerancia")

    # Cria um dicionário vazio para guardar as coordenadas
    grupos = {}

    # Ordena a lista
    pontos = OrdenarPontos(pontos, coordenada, inverter)

    # Itera sobre a lista de pontos
    for ponto in pontos:
        # Checa se a coordenada do ponto esta dentro da tolerância de algum grupo existente
        for grupoCoordenada in grupos:
            if abs(ponto[coordenada] - grupoCoordenada) <= tolerancia:
                # Se existir um grupo então adiciona o ponto a ele
                grupos[grupoCoordenada].append(ponto)
                break
        else:
            # Se não então criar um novo grupo
            grupos[ponto[coordenada]] = [ponto]

    # Retorna a lista de grupos ordenados
    return list(grupos.values())


def OrdenarPontos(pontos, coordenada, inverter=False):
    print('OrdenarPontos')
    # Organiza os pontos pela coordenada escolhida em ordem crescente ou decrescente
    pontosOrdenados = sorted(
        pontos, key=lambda p: p[coordenada], reverse=inverter)

    # Retorna os pontos ordenados
    return pontosOrdenados


def PlanificarLista(lista):
    resultado = []
    for elemento in lista:
        if type(elemento) == list:
            resultado.extend(PlanificarLista(elemento))
        else:
            resultado.append(elemento)
    return resultado


def PlanificarListaDePontos(pontos):
    print('PlanificarListaDePontos')
    listaPlanificada = PlanificarLista(pontos)

    subListas = []

    for i in range(0, len(listaPlanificada), 3):
        subLista = listaPlanificada[i:i+3]
        subListas.append(subLista)

    return subListas


def PegarLocalizacaoDosComponentes(componentes):
    print("PegarLocalizacaoDosComponentes")

    locacoes = []

    for component in componentes:
        component = unreal.StaticMeshComponent.cast(component)
        # componentLocation = component.relative_location
        componentLocation = component.get_local_bounds()[0].add(
            component.get_local_bounds()[1]).divide_int(2)
        locacoes.append(
            [componentLocation.x, componentLocation.y, componentLocation.z])

    return locacoes


def CriarTrackPadraoInicial(actor, levelSequence):
    # print("CriarTrackPadraoInicial")

    # Adiciona o primeiro componente do ator como uma track
    actorComponent = actor.get_component_by_class(unreal.StaticMeshComponent)
    componentBinding = levelSequence.add_possessable(actorComponent)

    return componentBinding


def CriarTrackVisibilidade(componentBinding, frameAntesDoInicial, frameInicial):
    # print("CriarTrackVisibilidade")

    # Adiciona uma track para alterar a visibilidade do ator
    visibilityTrack = componentBinding.get_parent(
    ).add_track(unreal.MovieSceneVisibilityTrack)

    # Adiciona uma seção com propriedade as tracks
    newSectionVisibility = visibilityTrack.add_section()

    # Cast as seçãos criadas para seus tipos corretos
    visibilitySection = unreal.MovieSceneBoolSection.cast(newSectionVisibility)

    # Pega todos os channels da seção
    channelsVisibility = visibilitySection.get_all_channels()

    # Cast o channel
    boolChannel = unreal.MovieSceneScriptingBoolChannel.cast(
        channelsVisibility[0])

    # Adiciona as chaves
    boolChannel.add_key(frameAntesDoInicial, False, 0,
                        unreal.SequenceTimeUnit.DISPLAY_RATE)
    boolChannel.add_key(frameInicial, True, 0,
                        unreal.SequenceTimeUnit.DISPLAY_RATE)

    # Define o range da seção
    visibilitySection.set_start_frame_bounded(True)
    visibilitySection.set_end_frame_bounded(True)

def CriarTrackVisibilidadeActor(componentBinding, frameAntesDoInicial, frameInicial):
    print("CriarTrackVisibilidadeActor")

    # Adiciona uma track para alterar a visibilidade do ator
    visibilityTrack = componentBinding.add_track(unreal.MovieSceneVisibilityTrack)
    print(visibilityTrack)
    # Adiciona uma seção com propriedade as tracks
    newSectionVisibility = visibilityTrack.add_section()
    print('2')
    # Cast as seçãos criadas para seus tipos corretos
    visibilitySection = unreal.MovieSceneBoolSection.cast(newSectionVisibility)
    print('3')
    # Pega todos os channels da seção
    channelsVisibility = visibilitySection.get_all_channels()
    print('4')
    # Cast o channel
    boolChannel = unreal.MovieSceneScriptingBoolChannel.cast(
        channelsVisibility[0])

    # Adiciona as chaves
    boolChannel.add_key(frameAntesDoInicial, False, 0,
                        unreal.SequenceTimeUnit.DISPLAY_RATE)
    boolChannel.add_key(frameInicial, True, 0,
                        unreal.SequenceTimeUnit.DISPLAY_RATE)

    # Define o range da seção
    visibilitySection.set_start_frame_bounded(True)
    visibilitySection.set_end_frame_bounded(True)

def CriarTrackVisibilidadeComponente(componentBinding, frameAntesDoInicial, frameInicial):
    # print("CriarTrackVisibilidadeComponente")

    # Adiciona uma track para alterar a visibilidade do ator
    visibilityTrack = componentBinding.add_track(
        unreal.MovieSceneVisibilityTrack)

    # Adiciona uma seção com propriedade as tracks
    newSectionVisibility = visibilityTrack.add_section()

    # Cast as seçãos criadas para seus tipos corretos
    visibilitySection = unreal.MovieSceneBoolSection.cast(newSectionVisibility)

    # Pega todos os channels da seção
    channelsVisibility = visibilitySection.get_all_channels()

    # Cast o channel
    boolChannel = unreal.MovieSceneScriptingBoolChannel.cast(
        channelsVisibility[0])

    # Adiciona as chaves
    boolChannel.add_key(frameAntesDoInicial, False, 0,
                        unreal.SequenceTimeUnit.DISPLAY_RATE)
    boolChannel.add_key(frameInicial, True, 0,
                        unreal.SequenceTimeUnit.DISPLAY_RATE)

    # Define o range da seção
    visibilitySection.set_start_frame_bounded(True)
    visibilitySection.set_end_frame_bounded(True)


def CriarTrackTrocaDeMaterial(componentBinding, actorComponent, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal):
    # print("CriarTrackVisibilidade")

    # Adiciona uma track para alterar o material do component
    materialChangeTrack = componentBinding.add_track(
        unreal.MovieScenePrimitiveMaterialTrack)

    # Adiciona uma seção com propriedade as tracks
    newSectionMaterial = materialChangeTrack.add_section()

    # Cast as seçãos criadas para seus tipos corretos
    materialChangeSection = unreal.MovieScenePrimitiveMaterialSection.cast(
        newSectionMaterial)

    # Pega todos os channels da seção
    channelsMaterial = materialChangeSection.get_all_channels()

    # Cast o channel
    materialChannel = unreal.MovieSceneScriptingObjectPathChannel.cast(
        channelsMaterial[0])

    # Pega os materiais originais do componente
    materialObjeto = unreal.StaticMeshComponent.cast(
        actorComponent).get_material(0)

    # Adiciona as chaves
    materialChannel.add_key(frameAntesDoInicial, materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
    materialChannel.add_key(frameFinal, materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
    materialChannel.add_key(frameAposOFinal, materialObjeto,0,unreal.SequenceTimeUnit.DISPLAY_RATE)

    # Define o range da seção
    materialChangeSection.set_start_frame_bounded(True)
    materialChangeSection.set_end_frame_bounded(True)


def CriarTrackTrocaDeMateriais(componentBinding, actorComponent, materialEfeito, frameAntesDoInicial, frameFinal, frameAposOFinal):
    # print("CriarTrackVisibilidade")

    # Pega os materiais originais do componente
    materials = unreal.StaticMeshComponent.cast(actorComponent).get_materials()

    print(f"QUANTIDADE DE MATERIAIS: {len(materials)}")

    for i in range(len(materials)):

        # Adiciona uma track para alterar o material do component
        materialChangeTrack = componentBinding.add_track(
            unreal.MovieScenePrimitiveMaterialTrack)
        unreal.MovieScenePrimitiveMaterialTrack.cast(
            materialChangeTrack).set_material_index(i)

        # Adiciona uma seção com propriedade as tracks
        newSectionMaterial = materialChangeTrack.add_section()

        # Cast as seçãos criadas para seus tipos corretos
        materialChangeSection = unreal.MovieScenePrimitiveMaterialSection.cast(
            newSectionMaterial)

        # Pega todos os channels da seção
        channelsMaterial = materialChangeSection.get_all_channels()

        # Cast o channel
        materialChannel = unreal.MovieSceneScriptingObjectPathChannel.cast(
            channelsMaterial[0])

        # Pega os materiais originais do componente
        materialObjeto = unreal.StaticMeshComponent.cast(
            actorComponent).get_material(i)

        # Adiciona as chaves
        materialChannel.add_key(frameAntesDoInicial, materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        materialChannel.add_key(frameFinal, materialEfeito,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        materialChannel.add_key(frameAposOFinal, materialObjeto,0,unreal.SequenceTimeUnit.DISPLAY_RATE)

        # Define o range da seção
        materialChangeSection.set_start_frame_bounded(True)
        materialChangeSection.set_end_frame_bounded(True)


def CriarTrackParametroDeMaterial(componentBinding, frameInicial, frameFinal):
    # print("CriarTrackVisibilidade")

    # Adiciona uma track para alterar o valor do material do component
    materialValueTrack = componentBinding.add_track(
        unreal.MovieSceneComponentMaterialTrack)

    # Adiciona uma seção com propriedade as tracks
    newSectionValue = materialValueTrack.add_section()

    # Cast as seçãos criadas para seus tipos corretos
    parameterSection = unreal.MovieSceneParameterSection.cast(newSectionValue)

    # Adiciona uma chave para criar automaticamente um channel e poder adicionar as chaves corretamente depois
    parameterSection.add_scalar_parameter_key(
        "Curve", unreal.FrameNumber(0), 0.0)

    # Pega todos os channels da seção
    channelsParameter = parameterSection.get_all_channels()

    # Cast o channel
    floatChannel = unreal.MovieSceneScriptingFloatChannel.cast(
        channelsParameter[0])

    # Adiciona as chaves corretamente
    floatChannel.add_key(frameInicial, 0.0, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)
    floatChannel.add_key(frameFinal, 2.0, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)

    # Remove a chave padrão
    chavePadrao = floatChannel.get_keys()[0]
    floatChannel.remove_key(chavePadrao)

    # Define o range da seção
    parameterSection.set_start_frame_bounded(True)
    parameterSection.set_end_frame_bounded(True)


def CriarTrackMoverElementoEmZ(actor, componentBinding, frameInicial, frameFinal):
    print("CriarTrackMoverElementoEmZ")

    actorMeioTamanho = unreal.Vector.cast(
        actor.get_actor_bounds(False, False)[1])

    # Adiciona uma track Transform ao ator
    elementMoveTrack = componentBinding.get_parent(
    ).add_track(unreal.MovieScene3DTransformTrack)

    # Refresh na Sequence para mostrar as alterações
    unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

    # Adiciona uma seção com propriedade as tracks
    transformSection = elementMoveTrack.add_section()

    # Cast as seçãos criadas para seus tipos corretos
    transformSection = unreal.MovieScene3DTransformSection.cast(
        transformSection)

    # Pega todos os channels da seção
    channelsTransform = transformSection.get_all_channels()

    for channel in channelsTransform:
        if channel.get_name().startswith("Location.Z"):
            print("Channel Location.Z")
            # Cast o channel
            doubleChannel = unreal.MovieSceneScriptingDoubleChannel.cast(
                channel)
            doubleChannel.add_key(frameInicial, actorMeioTamanho.z * 2, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)
            doubleChannel.add_key(frameFinal, 0, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)

    # Define o range da seção
    transformSection.set_start_frame_bounded(True)
    transformSection.set_end_frame_bounded(True)


def CriarTrackMoverComponenteEmZ(actor, component, componentBinding, frameInicial, frameFinal):
    # print("CriarTrackMoverComponenteEmZ")

    actorMeioTamanho = unreal.Vector.cast(
        actor.get_actor_bounds(False, False)[1])

    componentBounds = component.get_local_bounds()
    componentAltura = componentBounds[1].z - componentBounds[0].z

    componentLocation = component.relative_location

    # Adiciona uma track Transform ao ator
    elementMoveTrack = componentBinding.add_track(
        unreal.MovieScene3DTransformTrack)

    # Refresh na Sequence para mostrar as alterações
    unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

    # Adiciona uma seção com propriedade as tracks
    transformSection = elementMoveTrack.add_section()

    # Cast as seçãos criadas para seus tipos corretos
    transformSection = unreal.MovieScene3DTransformSection.cast(
        transformSection)

    # Pega todos os channels da seção
    channelsTransform = transformSection.get_all_channels()

    for channel in channelsTransform:
        if channel.get_name().startswith("Location.Z"):
            # Cast o channel
            doubleChannel = unreal.MovieSceneScriptingDoubleChannel.cast(
                channel)
            # doubleChannel.add_key(frameInicial, actorMeioTamanho.z * 2,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
            doubleChannel.add_key(
                frameInicial, componentAltura, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)
            doubleChannel.add_key(frameFinal, componentLocation.z, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        if channel.get_name().startswith("Location.X"):
            # Cast o channel
            doubleChannel = unreal.MovieSceneScriptingDoubleChannel.cast(
                channel)
            doubleChannel.add_key(
                frameInicial, componentLocation.x, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)
            doubleChannel.add_key(frameFinal, componentLocation.x, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        if channel.get_name().startswith("Location.Y"):
            # Cast o channel
            doubleChannel = unreal.MovieSceneScriptingDoubleChannel.cast(
                channel)
            doubleChannel.add_key(
                frameInicial, componentLocation.y, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)
            doubleChannel.add_key(
                frameFinal, componentLocation.y, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)

    # Define o range da seção
    transformSection.set_start_frame_bounded(True)
    transformSection.set_end_frame_bounded(True)


def CriarTrackMoverComponenteEmZAteValor(actor, component, componentBinding, frameInicial, frameFinal):
    # print("CriarTrackMoverComponenteEmZ")

    actorMeioTamanho = unreal.Vector.cast(
        actor.get_actor_bounds(False, False)[1])

    componentBounds = component.get_local_bounds()
    componentAltura = componentBounds[1].z - componentBounds[0].z

    componentLocation = component.relative_location

    # Adiciona uma track Transform ao ator
    elementMoveTrack = componentBinding.add_track(
        unreal.MovieScene3DTransformTrack)

    # Refresh na Sequence para mostrar as alterações
    unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

    # Adiciona uma seção com propriedade as tracks
    transformSection = elementMoveTrack.add_section()

    # Cast as seçãos criadas para seus tipos corretos
    transformSection = unreal.MovieScene3DTransformSection.cast(
        transformSection)

    # Pega todos os channels da seção
    channelsTransform = transformSection.get_all_channels()

    for channel in channelsTransform:
        if channel.get_name().startswith("Location.Z"):
            # Cast o channel
            doubleChannel = unreal.MovieSceneScriptingDoubleChannel.cast(
                channel)
            # doubleChannel.add_key(frameInicial, actorMeioTamanho.z * 2,0,unreal.SequenceTimeUnit.DISPLAY_RATE)
            doubleChannel.add_key(
                frameInicial, componentAltura, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)
            doubleChannel.add_key(frameFinal, componentLocation.z, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        if channel.get_name().startswith("Location.X"):
            # Cast o channel
            doubleChannel = unreal.MovieSceneScriptingDoubleChannel.cast(
                channel)
            doubleChannel.add_key(
                frameInicial, componentLocation.x, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)
            doubleChannel.add_key(frameFinal, componentLocation.x, 0,unreal.SequenceTimeUnit.DISPLAY_RATE)
        if channel.get_name().startswith("Location.Y"):
            # Cast o channel
            doubleChannel = unreal.MovieSceneScriptingDoubleChannel.cast(
                channel)
            doubleChannel.add_key(
                frameInicial, componentLocation.y, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)
            doubleChannel.add_key(
                frameFinal, componentLocation.y, 0, unreal.SequenceTimeUnit.DISPLAY_RATE)

    # Define o range da seção
    transformSection.set_start_frame_bounded(True)
    transformSection.set_end_frame_bounded(True)


# endregion

print('----- MEU CÓDIGO INICIA AQUI -----')

print('----- MEU CÓDIGO TERMINA AQUI -----')
